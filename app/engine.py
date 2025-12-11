# engine.py
from typing import Callable, Dict, Any, List
import asyncio

NodeFunc = Callable[[Dict[str, Any], Dict[str, Callable]], Any]

class Graph:
    def __init__(self, nodes, edges, start_node):
        self.nodes = nodes
        self.edges = edges
        self.start_node = start_node

class Runner:
    def __init__(self, graph: Graph, tools: Dict[str, Callable]):
        self.graph = graph
        self.tools = tools
        self.execution_log: List[str] = []

    async def run(self, initial_state: Dict[str, Any], max_steps: int = 1000):
        state = dict(initial_state)
        current = self.graph.start_node
        steps = 0

        while current and steps < max_steps:
            steps += 1
            self.execution_log.append(f"STEP {steps}: Running node '{current}'")

            node_fn = self.graph.nodes[current]
            result = node_fn(state, self.tools)
            if asyncio.iscoroutine(result):
                result = await result

            # Determine next node
            if isinstance(result, dict) and "next" in result:
                current = result["next"]
            elif isinstance(result, dict) and result.get("stop", False):
                break
            else:
                edge = self.graph.edges.get(current)
                current = edge(state) if callable(edge) else edge

            # Log a short snapshot
            self.execution_log.append(f"After step {steps}, snapshot: {self._short_state(state)}")

        return {"final_state": state, "log": self.execution_log}

    @staticmethod
    def _short_state(state):
        return {k: (v if isinstance(v, (int, float, bool)) or len(str(v)) < 80 else str(v)[:80]+"...") for k,v in state.items()}
