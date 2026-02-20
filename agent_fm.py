import re
import json

# ---------------------------------------------------------
# BASIC ABAP FM PARSER (stable, pattern-based)
# ---------------------------------------------------------

def parse_fm_source(text: str) -> dict:
    """
    Extract FM name, importing/exporting/changing/tables parameters
    using simple regex-based scanning.
    """

    fm_name_match = re.search(r"FUNCTION\s+(\w+)", text, re.IGNORECASE)
    if not fm_name_match:
        raise ValueError("Could not find FUNCTION <name> in source.")

    fm_name = fm_name_match.group(1)

    def extract_block(name):
        pattern = rf"{name}\s*([\s\S]*?)(?=(IMPORTING|EXPORTING|CHANGING|TABLES|EXCEPTIONS|\.)|ENDFUNCTION)"
        m = re.search(pattern, text, re.IGNORECASE)
        if not m:
            return []
        block = m.group(1).strip()
        lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
        params = []
        for ln in lines:
            parts = ln.split()
            if len(parts) >= 2:
                params.append({"name": parts[0], "type": " ".join(parts[1:])})
        return params

    result = {
        "fm_name": fm_name,
        "importing": extract_block("IMPORTING"),
        "exporting": extract_block("EXPORTING"),
        "changing": extract_block("CHANGING"),
        "tables": extract_block("TABLES"),
        "exceptions": extract_block("EXCEPTIONS"),
    }

    return result

# ---------------------------------------------------------
# JSON GENERATOR
# ---------------------------------------------------------

def generate_json_spec(fm_dict: dict) -> str:
    return json.dumps(fm_dict, indent=4)

# ---------------------------------------------------------
# MARKDOWN DOC GENERATOR
# ---------------------------------------------------------

def generate_markdown_doc(fm: dict) -> str:
    lines = []
    lines.append(f"# Function Module: {fm['fm_name']}\n")

    def write_section(title, items):
        lines.append(f"## {title}")
        if not items:
            lines.append("_None_\n")
            return
        for p in items:
            lines.append(f"- **{p['name']}** — {p['type']}")
        lines.append("")

    write_section("Importing Parameters", fm.get("importing"))
    write_section("Exporting Parameters", fm.get("exporting"))
    write_section("Changing Parameters", fm.get("changing"))
    write_section("Tables Parameters", fm.get("tables"))
    write_section("Exceptions", fm.get("exceptions"))

    return "\n".join(lines)

# ---------------------------------------------------------
# PYTHON STUB GENERATOR
# ---------------------------------------------------------

def generate_python_stub(fm: dict) -> str:
    name = fm["fm_name"].lower()

    params = []
    for section in ["importing", "changing", "tables"]:
        for p in fm.get(section, []):
            params.append(p["name"].lower())

    params_str = ", ".join(params) if params else ""

    stub = [
        f"def {name}({params_str}):",
        f"    \"\"\"Python stub for ABAP FM {fm['fm_name']}\"\"\"",
        f"    # TODO: Implement logic",
        f"    return None",
    ]

    return "\n".join(stub)

# ---------------------------------------------------------
# PYTEST STUB GENERATOR
# ---------------------------------------------------------

def generate_pytest_stub(fm: dict) -> str:
    py_name = fm["fm_name"].lower()
    return (
        "import pytest\n\n"
        f"from fm_stub import {py_name}\n\n"
        f"def test_{py_name}():\n"
        f"    # TODO: Adjust parameters\n"
        f"    result = {py_name}()\n"
        f"    assert result is None\n"
    )
