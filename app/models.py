# models.py
from pydantic import BaseModel
from typing import Dict, Any

class GraphCreateRequest(BaseModel):
    name: str

class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]
