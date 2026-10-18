"""Local, offline tests for app.py session-saving behavior.

These tests use fake OpenAI dependencies and fake input values.  They never read
.env, never make network calls, and never require API credits.  All generated
session files are written inside a temporary directory.
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

# Inject minimal fake dependencies before importing app.py.  This keeps the tests
# runnable even when openai/python-dotenv are not installed.
if "dotenv" not in sys.modules:
    dotenv_module = type(sys)("dotenv")
    dotenv_module.load_dotenv = lambda *args, **kwargs: None
    sys.modules["dotenv"] = dotenv_module

if "openai" not in sys.modules:
    openai_module = type(sys)("openai")
    openai_module.OpenAI = object
    sys.modules["openai"] = openai_module

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import app


class _FakeCompletions:
    def __init__(self, *, fail=False):
        self.fail = fail

    def create(self, **kwargs):
        if self.fail:
            raise RuntimeError("insufficient_quota")
        return _FakeResponse()


class _FakeResponse:
    def __init__(self):
        self.choices = [_FakeChoice()]


class _FakeChoice:
    def __init__(self):
        self.message = _FakeMessage()


class _FakeMessage:
    content = "demo session"


class SessionSavingTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()

    def test_save_session_history_creates_directory_and_file(self):
        history_path = os.path.join("sessions", "history.json")
        history = [{"role": "user", "content": "hello"}]

        app.save_session_history(history, history_path)

        self.assertTrue(os.path.exists(history_path))
        with open(history_path, encoding="utf-8") as file:
            self.assertEqual(json.load(file), history)

    def test_save_session_index_writes_index_file(self):
        index = {"demo_session": "1234"}
        app.save_session_index(index, "session_index.json")

        self.assertTrue(os.path.exists("session_index.json"))
        with open("session_index.json", encoding="utf-8") as file:
            self.assertEqual(json.load(file), index)

    def test_successful_new_session_creates_history_and_index(self):
        fake_client = _make_client(fail=False)
        app.get_openai_client = lambda: fake_client
        values = ["", "hello", "exit"]
        app.input = lambda prompt="": values.pop(0)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            app.main()

        self.assertTrue(os.path.exists("session_index.json"))
        with open("session_index.json", encoding="utf-8") as file:
            index = json.load(file)

        self.assertEqual(len(index), 1)
        session_id = next(iter(index.values()))
        history_path = os.path.join("sessions", f"{session_id}.json")
        self.assertTrue(os.path.exists(history_path))

        with open(history_path, encoding="utf-8") as file:
            history = json.load(file)
        self.assertEqual(
            history,
            [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "demo session"},
            ],
        )
        self.assertIn("Assistant:", output.getvalue())

    def test_failed_new_session_creates_no_files(self):
        fake_client = _make_client(fail=True)
        app.get_openai_client = lambda: fake_client
        values = ["", "hello"]
        app.input = lambda prompt="": values.pop(0)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            app.main()

        self.assertFalse(os.path.exists("session_index.json"))
        self.assertFalse(os.path.exists("sessions"))
        combined_output = output.getvalue()
        self.assertIn("Could not generate a session name", combined_output)
        self.assertIn("API error", combined_output)
        self.assertIn("insufficient_quota", combined_output)


def _make_client(*, fail):
    return type(
        "FakeClient",
        (),
        {"chat": type("FakeChat", (), {"completions": _FakeCompletions(fail=fail)})()},
    )()


if __name__ == "__main__":
    unittest.main()
