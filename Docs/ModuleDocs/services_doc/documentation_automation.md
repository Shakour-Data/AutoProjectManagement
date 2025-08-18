# Documentation Automation Module

## Overview
The `documentation_automation` module automates the generation of changelogs and release notes using GitHub integration. It handles retries and error logging to ensure reliable documentation updates.

## Class: DocumentationAutomation

### Description
The `DocumentationAutomation` class uses a `GitHubIntegration` instance to fetch commit data and generate changelogs and release notes. It supports retrying on failures and logs errors.

### Methods

- `__init__(self, github_integration, max_retries=3, retry_delay=2)`
  - Initializes the automation with GitHub integration and retry settings.

- `generate_changelog(self, since_date=None)`
  - Generates a changelog string of commits since a given date.
  - Retries on failure up to max_retries.

- `generate_release_notes(self, tag_name)`
  - Generates release notes for a given tag name.

## Diagrams

### Mermaid Class Diagram

```mermaid
classDiagram
    class DocumentationAutomation {
        - github: GitHubIntegration
        - max_retries: int
        - retry_delay: int
        - logger: Logger
        + __init__(github_integration, max_retries=3, retry_delay=2)
        + generate_changelog(since_date=None)
        + generate_release_notes(tag_name)
    }
    class GitHubIntegration
    DocumentationAutomation --> GitHubIntegration
```

### Changelog Generation Flowchart

```mermaid
flowchart TD
    A[Start] --> B[Initialize retries to 0]
    B --> C{Retries < max_retries?}
    C -- Yes --> D[Fetch commits from GitHub]
    D --> E[Filter commits by since_date]
    E --> F[Format changelog entries]
    F --> G[Return changelog]
    C -- No --> H[Log failure and return empty string]
    G --> I[Stop]
    H --> I[Stop]
```

---

## Credits

This module depends on the `GitHubIntegration` module for interacting with GitHub APIs.

---

This documentation provides a detailed overview of the `documentation_automation` module to assist developers in understanding and using its functionality effectively.
