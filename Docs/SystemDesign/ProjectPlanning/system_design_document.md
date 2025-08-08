# System Design Document

*Last updated: 2025-07-27*

## 1. Introduction

### 1.1 Purpose
This document describes the architecture and design of the ProjectManagement system, providing a blueprint for development and future maintenance.

### 1.2 Scope
Covers system architecture, components, interfaces, data flow, and design decisions.

### 1.3 Definitions, Acronyms, and Abbreviations
- API: Application Programming Interface
- CLI: Command Line Interface
- CI/CD: Continuous Integration/Continuous Deployment
- PMBOK: Project Management Body of Knowledge
- WBS: Work Breakdown Structure

## 2. System Architecture

### 2.1 Overview
The system is a modular, Python-based application integrating with GitHub and VS Code. It consists of backend services, a VS Code extension, and automation workflows.

### 2.2 Components
- Backend API: FastAPI-based RESTful services handling core logic, user input parsing, task prioritization, scheduling, progress tracking, and GitHub integration.
- VS Code Extension: Provides chat interface for informal user inputs and displays real-time updates and notifications.
- Automation Workflows: GitHub Actions for CI/CD pipelines, report generation, notifications, and scheduled tasks.
- Data Storage: Local project files, JSON input/output files, and GitHub repositories.

### 2.3 Architecture Diagram
*(Include diagram here if available)*

## 3. System Components Design

### 3.1 Backend API
- Handles task parsing, prioritization, scheduling, progress tracking, and user input management.
- Manages GitHub API interactions for issues, pull requests, projects, and workflow automation.
- Provides endpoints for project management, WBS levels, resources, allocations, and project start dates.

### 3.2 VS Code Extension
- Provides chat interface for informal user inputs.
- Displays real-time updates, notifications, and progress reports.

### 3.3 Automation Workflows
- Implements CI/CD pipelines using GitHub Actions.
- Automates report generation, notifications, and scheduled tasks such as daily progress updates.

## 4. Data Design

### 4.1 Data Models
- Task: Attributes include ID, description, status, priority, dependencies, and scheduling details.
- User: Roles, permissions, and access control.
- Resource: Human resources, equipment, materials, and availability.
- Project: Metadata, timelines, milestones, and aggregated metrics.

### 4.2 Data Flow
- User inputs via VS Code chat are parsed into formal tasks by the backend API.
- Tasks are synchronized with GitHub Issues and Projects for tracking.
- Progress updates flow from commit history and workflow execution to dashboards and reports.
- JSON input files for WBS parts, resources, allocations, and project start dates are managed and aggregated.

## 5. Interface Design

### 5.1 User Interface
- VS Code chat interface for task input, feedback, and progress monitoring.
- CLI commands for setup, status checks, task updates, and report generation.

### 5.2 External Interfaces
- GitHub API for project management integration including issues, pull requests, projects, and actions.
- VS Code Extension API for chat interface and notifications.

## 6. Security Design

- Secure storage and encrypted handling of authentication tokens.
- Role-based access control for multi-user permissions.
- Compliance with GitHub API rate limits and best practices.

## 7. Performance Considerations

- Efficient API calls and data processing to minimize latency.
- Scalability to support multiple projects, users, and concurrent operations.

## 8. Design Decisions and Rationale

- Use of FastAPI for a lightweight, modular backend service.
- Deep integration with GitHub to leverage existing project management features.
- VS Code extension for seamless and user-friendly interaction.
- Automation workflows to reduce manual overhead and ensure continuous updates.

## 9. Appendices

- Glossary of terms.
- References to related documents and standards.

## 10. Revision History

| Version | Date       | Description               | Author       |
|---------|------------|---------------------------|--------------|
| 1.2     | 2025-07-27 | Updated to reflect current implementation | Project Team |
