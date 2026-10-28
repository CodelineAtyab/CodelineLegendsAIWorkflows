# LangGraph Video Scenarios

Small, offline examples based on the graph exercises and agent workflows in
the LangGraph course linked from issue #257. Model calls, external APIs,
embeddings, and interactive input are replaced with deterministic Python so
each workflow can run without credentials.

Run a scenario from this directory with:

```sh
uv run scenario_01_number_guessing_loop.py
```

Each scenario prints the final state and writes its graph diagram beside the
script. See [`SCENARIOS.md`](SCENARIOS.md) for timestamps, graph shapes, and
adaptations.
