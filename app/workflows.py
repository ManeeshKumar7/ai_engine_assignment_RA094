# workflows.py
from engine import Graph
from typing import Dict, Any
from tools import TOOLS

def node_extract(state: Dict[str, Any], tools):
    code = state.get("code", "")
    state["functions"] = tools["extract_functions"](code)["functions"]
    return {}

def node_check_complexity(state: Dict[str, Any], tools):
    code = state.get("code", "")
    c = tools["complexity_score"](code)["complexity"]
    state["complexity"] = c
    state.setdefault("quality_score", 0)
    state["quality_score"] += max(0, 10 - c)
    return {}

def node_detect_issues(state: Dict[str, Any], tools):
    code = state.get("code", "")
    issues = tools["detect_smells"](code)["issues"]
    state["issues"] = issues
    state["quality_score"] -= issues
    return {}

def node_suggest(state: Dict[str, Any], tools):
    suggestions = []
    if state.get("issues", 0) > 0:
        suggestions.append("Remove debug prints, TODOs, eval()")
    if state.get("complexity", 0) > 5:
        suggestions.append("Reduce function complexity")
    state["suggestions"] = suggestions
    return {}

def node_check_stop(state: Dict[str, Any], tools):
    threshold = state.get("threshold", 7)
    if state.get("quality_score", 0) >= threshold:
        return {"stop": True}
    # Simulate a refinement step (improves quality slightly)
    state["quality_score"] = state.get("quality_score", 0) + 1
    return {"next": "detect_issues"}

def build_code_review_graph():
    nodes = {
        "extract": node_extract,
        "complexity": node_check_complexity,
        "detect_issues": node_detect_issues,
        "suggest": node_suggest,
        "check_stop": node_check_stop,
    }

    edges = {
        "extract": "complexity",
        "complexity": "detect_issues",
        "detect_issues": "suggest",
        "suggest": "check_stop",
        "check_stop": lambda state: None,
    }

    return Graph(nodes, edges, "extract"), TOOLS
