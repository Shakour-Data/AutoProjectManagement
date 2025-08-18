# extend_database_for_scrum Module

## Overview
The `extend_database_for_scrum` module extends the existing SQLite database schema with Scrum-specific tables to support agile project management. It adds tables for sprints, backlog items, and burndown data.

## Functions

- `connect_db()`
  - Connects to the SQLite database at the configured path.
  - Returns: SQLite connection object.

- `extend_schema_for_scrum(conn)`
  - Extends the database schema by creating Scrum-related tables if they do not exist:
    - `sprints`: Stores sprint details including ID, name, start/end dates, goal, and status.
    - `backlog_items`: Stores backlog items with references to sprints, status, priority, and timestamps.
    - `burndown_data`: Stores burndown chart data with remaining work per sprint and date.
  - Parameters:
    - `conn`: SQLite connection object.

- `main()`
  - Connects to the database and calls `extend_schema_for_scrum`.
  - Prints confirmation message.

## Usage
Run the module as a script to extend the database schema with Scrum tables:

```python
if __name__ == "__main__":
    main()
```

---

This documentation provides an overview of the `extend_database_for_scrum` module to assist developers in managing Scrum-specific database schema extensions.
