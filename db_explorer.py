import os
from fastmcp import FastMCP
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

mcp = FastMCP("Universal Database Co-Pilot")

def get_engine(db_target: str = "dev.db") -> Engine:
    """
    Resolves connection targets to a SQLAlchemy Engine.
    Supports local filenames ('dev.db') or full SQL URIs:
    - PostgreSQL: 'postgresql://user:pass@localhost:5432/mydb'
    - MySQL: 'mysql+pymysql://user:pass@localhost:3306/mydb'
    """
    if "://" not in db_target:
        safe_db_name = os.path.basename(db_target)
        if not safe_db_name.endswith(".db") and not safe_db_name.endswith(".sqlite"):
            safe_db_name += ".db"
        return create_engine(f"sqlite:///{safe_db_name}")
    return create_engine(db_target)

def mask_sensitive_data(col_name: str, val: object) -> str:
    """Masks PII and sensitive values in query results."""
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
def get_schema_diagram(db_target: str = "dev.db") -> str:
    """Generates a visual Mermaid.js ER diagram for ANY SQL database engine."""
    engine = get_engine(db_target)
    inspector = inspect(engine)
    
    mermaid = ["erDiagram"]
    for table_name in inspector.get_table_names():
        mermaid.append(f"    {table_name} {{")
        for col in inspector.get_columns(table_name):
            col_type = str(col['type'])
            col_name = col['name']
            mermaid.append(f"        {col_type} {col_name}")
        mermaid.append("    }")
    return f"### Schema Diagram (`{db_target}`)\n```mermaid\n" + "\n".join(mermaid) + "\n```"

@mcp.tool()
def generate_typescript_types(db_target: str = "dev.db") -> str:
    """Generates TypeScript interfaces for all tables in ANY SQL database engine."""
    engine = get_engine(db_target)
    inspector = inspect(engine)
    
    ts_output = []
    for table in inspector.get_table_names():
        interface_name = table.capitalize()[:-1] if table.endswith('s') else table.capitalize()
        ts_output.append(f"export interface {interface_name} {{")
        for col in inspector.get_columns(table):
            col_type_str = str(col['type']).upper()
            if any(t in col_type_str for t in ["INT", "FLOAT", "DOUBLE", "DECIMAL", "NUMERIC", "REAL"]):
                ts_type = "number"
            elif any(t in col_type_str for t in ["BOOL"]):
                ts_type = "boolean"
            elif any(t in col_type_str for t in ["BLOB", "BYTEA", "BINARY"]):
                ts_type = "any"
            else:
                ts_type = "string"
            ts_output.append(f"  {col['name']}: {ts_type};")
        ts_output.append("}\n")
    return "\n".join(ts_output)

@mcp.tool()
def generate_pydantic_models(db_target: str = "dev.db") -> str:
    """Generates Python Pydantic v2 models for all tables in ANY SQL database engine."""
    engine = get_engine(db_target)
    inspector = inspect(engine)
    
    py_output = ["from pydantic import BaseModel\nfrom typing import Optional\n"]
    for table in inspector.get_table_names():
        model_name = table.capitalize()[:-1] if table.endswith('s') else table.capitalize()
        py_output.append(f"class {model_name}(BaseModel):")
        for col in inspector.get_columns(table):
            col_type_str = str(col['type']).upper()
            if any(t in col_type_str for t in ["INT"]):
                py_type = "int"
            elif any(t in col_type_str for t in ["FLOAT", "DOUBLE", "DECIMAL", "NUMERIC", "REAL"]):
                py_type = "float"
            elif any(t in col_type_str for t in ["BOOL"]):
                py_type = "bool"
            elif any(t in col_type_str for t in ["BLOB", "BYTEA", "BINARY"]):
                py_type = "bytes"
            else:
                py_type = "str"
            py_output.append(f"    {col['name']}: {py_type}")
        py_output.append("")
    return "\n".join(py_output)

@mcp.tool()
def explain_query_plan(query: str, db_target: str = "dev.db") -> str:
    """Analyzes SQL query execution performance across database engines."""
    if not query.strip().lower().startswith("select"):
        return "Error: Only SELECT queries are supported."
    engine = get_engine(db_target)
    dialect = engine.dialect.name
    
    explain_cmd = f"EXPLAIN QUERY PLAN {query}" if dialect == "sqlite" else f"EXPLAIN {query}"
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(explain_cmd))
            rows = result.fetchall()
            plan_lines = [str(r) for r in rows]
            return f"Execution Plan (`{db_target}` - Dialect: `{dialect}`):\n" + "\n".join([f"- {line}" for line in plan_lines])
    except Exception as e:
        return f"Database Error on `{db_target}`: {str(e)}"

@mcp.tool()
def run_read_query_markdown(query: str, db_target: str = "dev.db", mask_pii: bool = True) -> str:
    """Executes a SELECT query on ANY SQL database engine with formatted Markdown output and optional PII masking."""
    if not query.strip().lower().startswith("select"):
        return "Error: Only SELECT queries allowed."
    engine = get_engine(db_target)
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            cols = list(result.keys())
            rows = result.fetchall()
            if not rows:
                return f"Query executed successfully on `{db_target}`. 0 rows returned."
            
            header = "| " + " | ".join(cols) + " |"
            divider = "| " + " | ".join(["---"] * len(cols)) + " |"
            
            body = []
            for row in rows:
                formatted_row = []
                for col, val in zip(cols, row):
                    cell_val = mask_sensitive_data(col, val) if mask_pii else str(val)
                    formatted_row.append(cell_val)
                body.append("| " + " | ".join(formatted_row) + " |")
                
            return f"**Database Target:** `{db_target}`\n\n" + "\n".join([header, divider] + body)
    except Exception as e:
        return f"Database Error on `{db_target}`: {str(e)}"

if __name__ == "__main__":
    mcp.run()
