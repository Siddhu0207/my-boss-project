import sqlite3
import os
from fastmcp import FastMCP

mcp = FastMCP("Advanced Database Co-Pilot")

def get_conn(db_name: str = "dev.db"):
    """Establishes a connection to the specified database with path traversal safety."""
    safe_db_name = os.path.basename(db_name)
    if not safe_db_name.endswith(".db") and not safe_db_name.endswith(".sqlite"):
        safe_db_name += ".db"
    return sqlite3.connect(safe_db_name)

def mask_sensitive_data(col_name: str, val: object) -> str:
    """Masks PII and sensitive values in output."""
    if val is None:
        return "NULL"
    val_str = str(val)
    col_lower = col_name.lower()
    
    if "email" in col_lower:
        parts = val_str.split("@")
        return f"{parts[0][0]}***@{parts[1]}" if len(parts) == 2 else "***"
    if any(k in col_lower for k in ["password", "secret", "token", "ssn", "credit_card"]):
        return "********"
    return val_str

@mcp.tool()
def get_schema_diagram(db_name: str = "dev.db") -> str:
    """Generates a visual Mermaid.js ER diagram of all tables and columns for any specified database."""
    conn = get_conn(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in cursor.fetchall() if not r[0].startswith("sqlite_")]
        
        mermaid = ["erDiagram"]
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            mermaid.append(f"    {table} {{")
            for col in cols:
                mermaid.append(f"        {col[2]} {col[1]}")
            mermaid.append("    }")
        return f"### Schema Diagram (`{db_name}`)\n```mermaid\n" + "\n".join(mermaid) + "\n```"
    finally:
        conn.close()

@mcp.tool()
def generate_typescript_types(db_name: str = "dev.db") -> str:
    """Generates TypeScript interfaces for all tables in any specified database."""
    type_map = {"INTEGER": "number", "REAL": "number", "TEXT": "string", "BLOB": "any"}
    conn = get_conn(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in cursor.fetchall() if not r[0].startswith("sqlite_")]
        
        ts_output = []
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            interface_name = table.capitalize()[:-1] if table.endswith('s') else table.capitalize()
            ts_output.append(f"export interface {interface_name} {{")
            for col in cols:
                ts_type = type_map.get(col[2].upper(), "string")
                ts_output.append(f"  {col[1]}: {ts_type};")
            ts_output.append("}\n")
        return "\n".join(ts_output)
    finally:
        conn.close()

@mcp.tool()
def generate_pydantic_models(db_name: str = "dev.db") -> str:
    """Generates Python Pydantic v2 models for all tables in any specified database."""
    type_map = {"INTEGER": "int", "REAL": "float", "TEXT": "str", "BLOB": "bytes"}
    conn = get_conn(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in cursor.fetchall() if not r[0].startswith("sqlite_")]
        
        py_output = ["from pydantic import BaseModel\nfrom typing import Optional\n"]
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            model_name = table.capitalize()[:-1] if table.endswith('s') else table.capitalize()
            py_output.append(f"class {model_name}(BaseModel):")
            for col in cols:
                py_type = type_map.get(col[2].upper(), "str")
                py_output.append(f"    {col[1]}: {py_type}")
            py_output.append("")
        return "\n".join(py_output)
    finally:
        conn.close()

@mcp.tool()
def explain_query_plan(query: str, db_name: str = "dev.db") -> str:
    """Analyzes SQL query performance using EXPLAIN QUERY PLAN on any specified database."""
    if not query.strip().lower().startswith("select"):
        return "Error: Only SELECT queries are supported."
    conn = get_conn(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute(f"EXPLAIN QUERY PLAN {query}")
        plan = cursor.fetchall()
        return f"Execution Plan (`{db_name}`):\n" + "\n".join([f"- {p[3]}" for p in plan])
    except Exception as e:
        return f"Database Error on `{db_name}`: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
def run_read_query_markdown(query: str, db_name: str = "dev.db", mask_pii: bool = True) -> str:
    """Executes a SELECT query and returns formatted Markdown table output with optional PII masking."""
    if not query.strip().lower().startswith("select"):
        return "Error: Only SELECT queries allowed."
    conn = get_conn(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        if not rows:
            return f"Query executed successfully on `{db_name}`. 0 rows returned."
        
        header = "| " + " | ".join(cols) + " |"
        divider = "| " + " | ".join(["---"] * len(cols)) + " |"
        
        body = []
        for row in rows:
            formatted_row = []
            for col, val in zip(cols, row):
                cell_val = mask_sensitive_data(col, val) if mask_pii else str(val)
                formatted_row.append(cell_val)
            body.append("| " + " | ".join(formatted_row) + " |")
            
        return f"**Database:** `{db_name}`\n\n" + "\n".join([header, divider] + body)
    except Exception as e:
        return f"Database Error on `{db_name}`: {str(e)}"
    finally:
        conn.close()

if __name__ == "__main__":
    mcp.run()
