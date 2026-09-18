import pytest
from db_explorer import (
    run_read_query_markdown,
    explain_query_plan,
    get_schema_diagram,
    generate_typescript_types
)

def test_select_query_allowed():
    """Verify valid SELECT queries run and return Markdown formatted data."""
    result = run_read_query_markdown("SELECT name FROM users LIMIT 1;")
    assert "Database Error" not in result
    assert "Alice Smith" in result

def test_security_guardrail_blocks_delete():
    """Verify write operations like DELETE are blocked by security guardrails."""
    result = run_read_query_markdown("DELETE FROM users;")
    assert "Error: Only SELECT queries allowed." in result

def test_security_guardrail_blocks_drop():
    """Verify DDL operations like DROP TABLE are blocked."""
    result = run_read_query_markdown("DROP TABLE users;")
    assert "Error: Only SELECT queries allowed." in result

def test_explain_query_plan():
    """Verify EXPLAIN QUERY PLAN analysis executes properly."""
    result = explain_query_plan("SELECT * FROM products;")
    assert "Execution Plan:" in result

def test_get_schema_diagram():
    """Verify Mermaid ER diagram code is generated correctly."""
    result = get_schema_diagram()
    assert "erDiagram" in result
    assert "users {" in result

def test_generate_typescript_types():
    """Verify TypeScript interface generation runs across schemas."""
    result = generate_typescript_types()
    assert "export interface" in result
    assert "id: number;" in result
