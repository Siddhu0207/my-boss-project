import sqlite3
from fastmcp import FastMCP

mcp = FastMCP("Advanced Database Co-Pilot")
DB_PATH = "dev.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

@mcp.tool()
def get_schema_diagram() -> str:
    """Generates a visual Mermaid.js ER diagram of all tables and columns."""
    conn = get_conn()
    cursor = conn.cursor()
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
    conn.close()
    return "```mermaid\n" + "\n".join(mermaid) + "\n```"

@mcp.tool()
def generate_typescript_types() -> str:
    """Generates TypeScript interfaces for all database tables."""
    type_map = {"INTEGER": "number", "REAL": "number", "TEXT": "string", "BLOB": "any"}
    conn = get_conn()
    cursor = conn.cursor()
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
    conn.close()
    return "\n".join(ts_output)

@mcp.tool()
def explain_query_plan(query: str) -> str:
    """Analyzes an SQL query performance using EXPLAIN QUERY PLAN."""
    if not query.strip().lower().startswith("select"):
        return "Error: Only SELECT queries are supported."
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(f"EXPLAIN QUERY PLAN {query}")
        plan = cursor.fetchall()
        conn.close()
        return "Execution Plan:\n" + "\n".join([f"- {p[3]}" for p in plan])
    except Exception as e:
        conn.close()
        return f"Database Error: {str(e)}"

@mcp.tool()
def run_read_query_markdown(query: str) -> str:
    """Executes a SELECT query and returns formatted Markdown table output."""
    if not query.strip().lower().startswith("select"):
        return "Error: Only SELECT queries allowed."
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return "Query executed successfully. 0 rows returned."
        
        header = "| " + " | ".join(cols) + " |"
        divider = "| " + " | ".join(["---"] * len(cols)) + " |"
        body = ["| " + " | ".join(str(val) for val in r) + " |" for r in rows]
        return "\n".join([header, divider] + body)
    except Exception as e:
        conn.close()
        return f"Database Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
