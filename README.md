# Mini Workflow Engine — AI Engineering Assignment (RA094)

This repository contains the implementation of a minimal workflow/agent execution engine built as part of the AI Engineering Assignment. The engine executes directed graphs where each node is a Python function operating on shared state. It supports branching, looping, tool usage, and exposes a FastAPI interface for creating and running workflows. A complete example workflow, the Code Review Mini-Agent, is included as required in the assignment.

---

## Overview

The workflow engine is designed to run simple, rule-based workflows represented as a directed graph. Each workflow is composed of nodes, edges, and a shared state dictionary. Nodes update the state, edges define execution flow, and the engine handles sequential execution, conditional branching, looping until conditions are met, and capturing logs at each step. This system models the core ideas of workflow engines used in agent frameworks, implemented in a lightweight and easy-to-extend manner.

---

## Engine Capabilities

**Nodes:**  
Functions that receive shared state, modify it, and return results or control instructions.

**Shared State:**  
A dictionary passed through all nodes, updated at each step to accumulate information.

**Edges:**  
Mappings that define which node runs next, making the workflow behave like a directed graph.

**Branching:**  
Nodes can choose different next steps based on conditions in the state.

**Looping:**  
Nodes may run repeatedly until a target condition or threshold is reached.

**Tool Registry:**  
Reusable helper tools stored in a registry, accessible by workflows.

**Execution Logs:**  
Each execution step is logged, allowing introspection of workflow behavior.

**REST API:**  
The entire engine is wrapped with FastAPI, exposing routes to create workflows, run them, and retrieve their state.

---

## Example Workflow: Code Review Mini-Agent

The repository includes an example workflow as required. The Code Review Mini-Agent analyzes Python code using simple rules.  
It performs the following steps:

1. Extracts function definitions from the input code  
2. Computes basic complexity metrics  
3. Detects issues such as TODOs, debug prints, and unused elements  
4. Generates suggestions for improvement  
5. Loops until a desired quality threshold is achieved  

This demonstrates node execution, branching logic, looping, and state updates in a clear manner.

---

## Project Structure


```
app/
 ├── engine.py        # Core workflow engine logic
 ├── workflows.py     # Code Review Mini-Agent workflow definition
 ├── tools.py         # Utility tools used by nodes
 ├── models.py        # Pydantic models for API requests/responses
 └── main.py          # FastAPI application exposing engine functionality
```

The structure keeps the engine modular, readable, and easy to extend with new workflows or tools.

---

## API Summary

The engine exposes a simple set of API endpoints:

- **POST /graph/create**  
  Creates a workflow graph and returns its ID.

- **POST /graph/run**  
  Runs a workflow with an initial state and returns a run ID.

- **GET /graph/state/{run_id}**  
  Fetches the final state, intermediate logs, and node-by-node execution history.

These endpoints allow external systems to interact with the workflow engine programmatically.

---

## What Can Be Improved in Future

- Persisting workflows and run history in a database  
- Visualizing workflow graphs and execution paths  
- Adding asynchronous execution support  
- Creating additional predefined workflows  
- Adding WebSocket-based live log streaming  
- Improving error handling and state validation  

---



## Author  
**Maneesh Kumar (RA094)**  
AI Engineering Assignment Submission  
