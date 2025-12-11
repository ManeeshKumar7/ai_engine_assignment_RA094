# tools.py
def detect_smells(code: str):
    issues = 0
    if "TODO" in code: issues += 1
    if "print(" in code: issues += 1
    if "eval(" in code: issues += 2
    return {"issues": issues}

def extract_functions(code: str):
    funcs = []
    for line in code.splitlines():
        if line.strip().startswith("def "):
            funcs.append(line.split("(")[0].replace("def ", "").strip())
    return {"functions": funcs}

def complexity_score(code: str):
    # crude complexity metric
    return {"complexity": max(1, len(code.splitlines()) // 5)}

TOOLS = {
    "detect_smells": detect_smells,
    "extract_functions": extract_functions,
    "complexity_score": complexity_score,
}
