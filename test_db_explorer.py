import pytest
from db_explorer import (
    run_read_query_markdown,
    explain_query_plan,
    get_schema_diagram,
    generate_typescript_types,
    generate_pydantic_models,
    mask_sensitive_data,
)

def test_select_query_allowed():
    """Verify valid SELECT queries run and return formatted Markdown data."""
    result = run_read_query_markdown("SELECT 1 AS test_col;", db_target="dev.db")
    assert "Database Error" not in result
    assert "test_col" in result

def test_security_guardrail_blocks_delete():
    """Verify write operations like DELETE are blocked by security guardrails."""
    result = run_read_query_markdown("DELETE FROM users;", db_target="dev.db")
    assert "Error: Only SELECT queries allowed." in result

def test_security_guardrail_blocks_drop():
    """Verify DDL operations like DROP TABLE are blocked."""
    result = run_read_query_markdown("DROP TABLE users;", db_target="dev.db")
    assert "Error: Only SELECT queries allowed." in result

def test_pii_masking_logic():
    """Verify sensitive fields like emails and passwords are redacted."""
    assert mask_sensitive_data("email", "john.doe@example.com") == "j***@example.com"
    assert mask_sensitive_data("user_password", "supersecret123") == "********"
    assert mask_sensitive_data("user_id", 101) == "101"

def test_get_schema_diagram():
    """Verify Mermaid ER diagram code is generated correctly."""
    result = get_schema_diagram("dev.db")
    assert "erDiagram" in result

def test_generate_typescript_types():
    """Verify TypeScript interface generation runs across schemas."""
    result = generate_typescript_types("dev.db")
    assert "export interface" in result

def test_generate_pydantic_models():
    """Verify Python Pydantic v2 BaseModel generation works."""
    result = generate_pydantic_models("dev.db")
    assert "class " in result
    assert "BaseModel" in result

def test_explain_query_plan():
    """Verify EXPLAIN QUERY PLAN analysis executes properly."""
    result = explain_query_plan("SELECT 1;", db_target="dev.db")
    assert "Execution Plan" in result

def test_multi_db_dynamic_target():
    """Verify the tool can target SQLite URI targets or secondary databases."""
    result = get_schema_diagram("sqlite:///dev.db")
    assert "erDiagram" in result
