Json Input Files Usage



# JSON Input Files and Their Usage in the Project Management System

## Introduction

This document provides a comprehensive and detailed description of the JSON input files used by the Project Management System. It explains the structure, purpose, and usage of each JSON file, along with examples and diagrams to facilitate understanding and effective use.

---

## Folder Structure and Detailed JSON Input Files

The JSON input files are organized under the `PM_JSON/` directory with the following subfolders:

* `user_inputs/`: Contains all JSON files provided or edited by users to define project tasks, resources, workflows, and planning data.
* `system_outputs/`: Contains JSON files generated or updated by the system during project execution and tracking.

## Below is a detailed description of each JSON input file located in the `user_inputs/` folder, including their precise structure, fields, and examples.

## 1. `detailed_wbs.json`

* **Purpose:** Defines the Work Breakdown Structure (WBS) with tasks, hierarchy, and relationships.
* **Structure:** An array of task objects with fields:
* `id` (string): Unique identifier for the task.
* `title` (string): Task title.
* `optimistic_hours` (number): Estimated optimistic duration.
* `normal_hours` (number): Estimated normal duration.
* `pessimistic_hours` (number): Estimated pessimistic duration.
* `predecessors` (array of strings, optional): IDs of predecessor tasks.
* `subtasks` (array): Nested subtasks with the same structure.
* **Example:**

```
[
  {
    "id": "1",
    "title": "Project Management System Development",
    "optimistic_hours": 0,
    "normal_hours": 0,
    "pessimistic_hours": 0,
    "subtasks": [
      {
        "id": "1.1",
        "title": "Python Package and Environment Setup",
        "optimistic_hours": 2,
        "normal_hours": 4,
        "pessimistic_hours": 6,
        "predecessors": ["0"],
        "subtasks": []
      }
    ]
  }
]

```

---

## 2. `human_resources.json`

* **Purpose:** Lists human resources involved in the project with detailed attributes.
* **Structure:** An array of resource objects with fields:
* `id` (string): Unique resource identifier.
* `name` (string): Full name.
* `role` (string): Role in the project.
* `department` (string): Department name.
* `hourly_rate` (number): Hourly cost rate.
* `email` (string): Contact email.
* `phone` (string): Contact phone number.
* `hire_date` (string, ISO date): Hiring date.
* `active` (boolean): Active status.
* `github_address` (string): GitHub profile URL.
* `gmail` (string): Gmail address.
* `gmail_password` (string): Encrypted Gmail password.
* `github_password` (string): Encrypted GitHub password.
* `github_token` (string): GitHub access token.
* **Security Note:** Sensitive fields such as passwords and tokens are stored encrypted. Handle these fields with care and ensure secure storage and access.
* **Example:**

```
[
  {
    "id": "HR001",
    "name": "Alice Johnson",
    "role": "Project Manager",
    "department": "Management",
    "hourly_rate": 60,
    "email": "alice.johnson@example.com",
    "phone": "+1234567890",
    "hire_date": "2022-01-15",
    "active": true,
    "github_address": "https://github.com/alicejohnson",
    "gmail": "alice.johnson@gmail.com",
    "gmail_password": "encrypted_password_here",
    "github_password": "encrypted_password_here",
    "github_token": "ghp_exampletoken1234567890"
  }
]

```

---

## Detailed Description of Key JSON Files

### 1. `wbs_data.json`

* Contains the Work Breakdown Structure (WBS) tasks.
* Each task has an `id`, `title`, `level`, optional `description`, and `subtasks`.
* Example snippet:

```
[
  {
    "id": "1",
    "title": "Project Setup",
    "level": 1,
    "subtasks": [
      {
        "id": "1.1",
        "title": "Create Python package structure",
        "level": 2,
        "subtasks": []
      }
    ]
  }
]

```

### 2. `wbs_scores.json`

* Contains importance and urgency scores for each task by `id`.
* Used for dynamic prioritization.
* Example snippet:

```
{
  "1.1": {
    "importance": 0.8,
    "urgency": 0.6
  }
}

```

### 3. `human_resources.json`

* Lists human resources with attributes such as name, role, availability.
* Example snippet:

```
[
  {
    "id": "hr1",
    "name": "Alice",
    "role": "Developer",
    "availability": 1.0
  }
]

```

### 4. `resource_allocation.json` and `task_resource_allocation.json`

* Define how resources are allocated to tasks.
* Include allocation percentages and roles.
* Example snippet:

```
[
  {
    "task_id": "1.1",
    "resource_id": "hr1",
    "allocation": 0.5
  }
]

```

### 5. `workflow_definition.json`

* Defines the ordered steps in workflows.
* Used to track task progress through stages.
* Example snippet:

```
[
  "To Do",
  "In Progress",
  "Code Review",
  "Done"
]

```

---

## Diagrams

### Task Hierarchy Diagram

```
Project Setup (id: 1)
├── Create Python package structure (id: 1.1)
├── Implement virtual environment (id: 1.2)
└── Automate configuration setup (id: 1.3)

```

### Resource Allocation Flow

```
[Human Resources] --> [Resource Allocation JSON] --> [Tasks]

```

---

## Best Practices

* Keep JSON files well-formatted and human-readable.
* Use consistent naming conventions.
* Validate JSON files against schemas before use.
* Maintain version control for JSON files.
* Handle missing or optional fields gracefully.
* Use parent-child references for hierarchical data instead of deep nesting.

---

## Summary

This document details the JSON input files used by the Project Management System, their structure, and usage. The system operates directly on these JSON files without a database, enabling flexible and dynamic project management workflows.

---

## JSON File Standards Documentation

To maintain clarity and ease of maintenance, detailed standards for each JSON input file are documented separately in the [`json_standards/`](./json_standards) folder. This folder contains individual markdown files describing the structure, purpose, and examples for each JSON file used in the system.

Please refer to the following documents for detailed standards:

* [detailed\_wbs.json Standard](./json_standards/detailed_wbs.md)
* [human\_resources.json Standard](./json_standards/human_resources.md)
* [wbs\_data.json Standard](./json_standards/wbs_data.md)
* [wbs\_scores.json Standard](./json_standards/wbs_scores.md)
* [resource\_allocation.json and task\_resource\_allocation.json Standard](./json_standards/resource_allocation.md)
* [workflow\_definition.json Standard](./json_standards/workflow_definition.md)

Additional JSON file standards will be added to this folder as needed.

---

Please refer to the consolidated JSON files relationships and usage document for a comprehensive overview of all JSON files, their data sources, formation, usage, and interrelationships:

* [JSON Files Overview, Relationships, and Usage](./json_files_overview.md)

For further assistance, please contact the project management office.

---