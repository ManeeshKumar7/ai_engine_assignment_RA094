# main.py
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from uuid import uuid4
from typing import Dict
from engine import Runner
from workflows import build_code_review_graph
from tools import TOOLS
from models import GraphCreateRequest, GraphRunRequest

app = FastAPI(title="Mini Workflow Engine")

# In-memory stores
GRAPHS: Dict[str, object] = {}
RUNNERS: Dict[str, Runner] = {}
RUN_STATES: Dict[str, dict] = {}

@app.post("/graph/create")
def create_graph(req: GraphCreateRequest):
    if req.name == "code_review":
        graph, tools = build_code_review_graph()
        graph_id = str(uuid4())
        GRAPHS[graph_id] = {"graph": graph, "tools": tools}
        return {"graph_id": graph_id}
    raise HTTPException(status_code=400, detail="Unknown graph name. Use 'code_review'.")

@app.post("/graph/run")
async def run_graph(req: GraphRunRequest, background_tasks: BackgroundTasks):
    entry = GRAPHS.get(req.graph_id)
    if not entry:
        raise HTTPException(status_code=404, detail="graph_id not found")
    graph = entry["graph"]
    tools = entry["tools"]

    run_id = str(uuid4())
    runner = Runner(graph, tools)
    RUNNERS[run_id] = runner
    RUN_STATES[run_id] = {"status": "running", "state": req.initial_state, "log": []}

    async def _run():
        result = await runner.run(req.initial_state)
        RUN_STATES[run_id]["status"] = "finished"
        RUN_STATES[run_id]["state"] = result["final_state"]
        RUN_STATES[run_id]["log"] = result["log"]

    background_tasks.add_task(_run)
    return {"run_id": run_id}

@app.get("/graph/state/{run_id}")
def graph_state(run_id: str):
    entry = RUN_STATES.get(run_id)
    if not entry:
        raise HTTPException(status_code=404, detail="run_id not found")
    return entry

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
