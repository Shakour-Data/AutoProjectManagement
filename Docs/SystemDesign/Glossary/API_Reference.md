# API Reference Document

*Last updated: 2025-07-27*

This document provides a detailed reference for the backend API endpoints of the ProjectManagement system. It describes each endpoint's purpose, HTTP method, URL path, parameters, request body, and response.

## Base URL

All endpoints are prefixed with:

```
/api/v1
```

---

## Endpoints

### 1. Projects

#### List Projects

- **Method:** GET
- **Path:** /projects
- **Description:** Retrieves a list of all projects.
- **Parameters:** None
- **Response:** List of project identifiers.

#### Create Project

- **Method:** POST
- **Path:** /projects
- **Description:** Creates a new project with the specified project ID.
- **Parameters:**
  - `project_id` (query, string, required): Unique project identifier.
- **Response:** Success or error message.

#### Delete Project

- **Method:** DELETE
- **Path:** /projects
- **Description:** Deletes the project with the specified project ID.
- **Parameters:**
  - `project_id` (query, string, required): Unique project identifier.
- **Response:** Success or error message.

---

### 2. WBS Levels

#### Get WBS Levels

- **Method:** GET
- **Path:** /user_inputs/wbs_levels
- **Description:** Retrieves the WBS levels for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Response:** List of WBSLevel objects.

#### Save WBS Levels

- **Method:** POST
- **Path:** /user_inputs/wbs_levels
- **Description:** Saves the WBS levels for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Request Body:** List of WBSLevel objects.
- **Response:** Success or error message.

#### Delete WBS Levels

- **Method:** DELETE
- **Path:** /user_inputs/wbs_levels
- **Description:** Deletes the WBS levels for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Response:** Success or error message.

---

### 3. Resources

#### Get Resources

- **Method:** GET
- **Path:** /user_inputs/resources
- **Description:** Retrieves the resources for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Response:** List of Resource objects.

#### Save Resources

- **Method:** POST
- **Path:** /user_inputs/resources
- **Description:** Saves the resources for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Request Body:** List of Resource objects.
- **Response:** Success or error message.

#### Delete Resources

- **Method:** DELETE
- **Path:** /user_inputs/resources
- **Description:** Deletes the resources for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Response:** Success or error message.

---

### 4. Allocations

#### Get Allocations

- **Method:** GET
- **Path:** /user_inputs/allocations
- **Description:** Retrieves the resource allocations for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Response:** List of Allocation objects.

#### Save Allocations

- **Method:** POST
- **Path:** /user_inputs/allocations
- **Description:** Saves the resource allocations for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Request Body:** List of Allocation objects.
- **Response:** Success or error message.

#### Delete Allocations

- **Method:** DELETE
- **Path:** /user_inputs/allocations
- **Description:** Deletes the resource allocations for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Response:** Success or error message.

---

### 5. Project Start Date

#### Get Project Start Date

- **Method:** GET
- **Path:** /user_inputs/project_start_date
- **Description:** Retrieves the project start date for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Response:** ProjectStartDate object.

#### Save Project Start Date

- **Method:** POST
- **Path:** /user_inputs/project_start_date
- **Description:** Saves the project start date for a given project.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Request Body:** ProjectStartDate object.
- **Response:** Success or error message.

---

### 6. Aggregate WBS

#### Aggregate WBS Parts

- **Method:** POST
- **Path:** /user_inputs/aggregate_wbs
- **Description:** Aggregates WBS parts JSON files into a detailed WBS JSON and generates Gantt chart data.
- **Parameters:**
  - `project_id` (query, string, required): Project identifier.
- **Response:** Success or error message with status.

---

# Data Models

## WBSLevel

- `id`: string
- `name`: string
- `parent_id`: string (optional)
- `duration_days`: integer (optional)

## Resource

- `id`: string
- `name`: string
- `type`: string
- `availability`: integer (optional)

## Allocation

- `wbs_id`: string
- `resource_id`: string
- `allocation_percentage`: float (0 to 100)

## ProjectStartDate

- `start_date`: string (ISO format date)

---

This concludes the API Reference Document.
