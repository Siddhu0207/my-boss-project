# Database Co-Pilot (MCP Tool for BOSS Console)

> **BOSS Console Hackathon Submission (EXTEND Track)**  
> **Demo Video:** [Link to Your 2-Minute Demo Video Here]

Database Co-Pilot is a secure, multi-engine Model Context Protocol (MCP) server built with **FastMCP** and **SQLAlchemy**. It transforms AI agents into developer-focused database administrators, enabling safe schema exploration, full-stack type generation (TypeScript & Pydantic v2), query performance analysis, and read-only data querying with automated PII masking.

---

## Problem & Solution

Giving AI agents raw, unconstrained database access poses major risks:
1. **Accidental Data Loss:** Unrestricted write access can lead to destructive operations (`DROP`, `DELETE`, `UPDATE`).
2. **PII & Data Leaks:** Sensitive customer fields (emails, passwords, API tokens) can contaminate LLM context windows and training logs.
3. **Developer Friction:** Hand-writing TypeScript interfaces or Pydantic models from database schemas takes manual effort and introduces typing bugs.

**Database Co-Pilot solves this by inserting a secure, intelligent abstraction layer between the AI agent and your database.**

---
## Key Features & MCP Tools

| Tool Name | Engine Support | Description |
| :--- | :--- | :--- |
| `get_schema_diagram` | Any SQL Engine | Generates visual Mermaid.js ER diagrams of tables, columns, and data types for instant chat rendering. |
| `generate_typescript_types` | Any SQL Engine | Inspects column metadata and emits type-safe TypeScript `interface` definitions for frontend apps. |
| `generate_pydantic_models` | Any SQL Engine | Generates Python Pydantic v2 `BaseModel` classes mapped directly to table schemas for backend APIs. |
| `explain_query_plan` | Dialect-Aware | Runs `EXPLAIN` / `EXPLAIN QUERY PLAN` commands to help developers debug slow queries and indexes. |
| `run_read_query_markdown` | Any SQL Engine | Safely executes `SELECT` queries, formats output into Markdown tables, and applies automated cell-level PII masking. |

---
## Enterprise Security & Guardrails

* **Read-Only Enforcement:** Strictly blocks non-`SELECT` statements (`DELETE`, `DROP`, `UPDATE`, `INSERT`, `ALTER`) at the tool entry point.
* **Automated PII Redaction:** The `mask_sensitive_data` engine inspects query outputs cell-by-cell before returning results:
  * **Emails:** Masked to `a***@domain.com` format.
  * **Secrets & Credentials:** Fields matching `password`, `secret`, `token`, `ssn`, or `credit_card` are converted to `********`.
* **Path Traversal Protection:** Enforces filename sanitization via `os.path.basename` to prevent unauthorized file system traversal.
* **Universal Database Support:** Built on **SQLAlchemy**, supporting zero-setup local SQLite databases (`dev.db`, `saas.db`) alongside enterprise SQL connections (`postgresql://`, `mysql://`, `mssql://`).

---
## Repository Structure

```text
my-boss-project/
├── db_explorer.py          # Core MCP server implementation (FastMCP + SQLAlchemy)
├── test_db_explorer.py     # 9-case pytest validation suite
├── dev.db                  # Primary sample dataset (Users, Products)
├── saas.db                 # Secondary sample dataset (Subscriptions, Billing)
├── requirements.txt        # Production dependencies
└── README.md               # Architecture documentation & visual output previews

 
 
    
