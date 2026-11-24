"""Save the compiled LangGraph diagrams next to the workflow modules.

Each workflow keeps two artifacts, matching the other LangGraph projects in
this repository:

    qdrant_rag/ingest_workflow.png   <- rendered graph (commit this)
    qdrant_rag/ingest_workflow.mmd   <- Mermaid source (commit this)
"""

from pathlib import Path

from langgraph.graph.state import CompiledStateGraph

GRAPH_DIR = Path(__file__).resolve().parent


def save_graph_artifacts(
    workflow: CompiledStateGraph,
    name: str,
    *,
    best_effort: bool = True,
) -> tuple[Path, Path]:
    """Write `<name>.mmd` and `<name>.png` into the package directory.

    Rendering the PNG uses the Mermaid web service, so it needs network access.
    With `best_effort=True` a failure is reported but never breaks a run.
    """
    stem = GRAPH_DIR / name
    mermaid_path = stem.with_suffix(".mmd")
    png_path = stem.with_suffix(".png")

    graph = workflow.get_graph()
    mermaid_path.write_text(graph.draw_mermaid(), encoding="utf-8")

    try:
        graph.draw_mermaid_png(
            output_file_path=str(png_path),
            background_color="white",
            padding=10,
        )
    except Exception as error:  # noqa: BLE001 - rendering is a nice-to-have
        if not best_effort:
            raise
        print(f"  ! could not render {png_path.name}: {error}")
        print(f"    Mermaid source is still available at {mermaid_path}")

    return png_path, mermaid_path


def ensure_graph_artifacts(
    workflow: CompiledStateGraph,
    name: str,
    *,
    best_effort: bool = True,
) -> tuple[Path, Path]:
    """Write the diagrams only when they are missing.

    Used by `ingest` and `query` so a normal run never depends on the Mermaid
    rendering service. `main.py graphs` refreshes them explicitly.
    """
    stem = GRAPH_DIR / name
    png_path = stem.with_suffix(".png")
    mermaid_path = stem.with_suffix(".mmd")
    if png_path.exists() and mermaid_path.exists():
        return png_path, mermaid_path
    return save_graph_artifacts(workflow, name, best_effort=best_effort)
