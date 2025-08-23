### Communication Risk Documentation Integration Module

- **Method:** N/A (Integration Module)
- **Path:** `/main_modules/communication_risk/communication_risk_doc_integration.py`
- **Description:** Integration module that combines communication risk management with documentation automation for GitHub repositories.
- **Authentication:** GitHub token (optional)
- **Rate Limit:** GitHub API rate limits apply

#### Class: CommunicationRiskDocIntegration

**Description:** Integrates risk management with documentation automation for comprehensive project communication and risk documentation.

**Constructor:**
```python
CommunicationRiskDocIntegration(repo_owner: str, repo_name: str, token: str = None)
```

**Parameters:**
- `repo_owner`: GitHub repository owner (organization or username)
- `repo_name`: GitHub repository name
- `token`: GitHub personal access token (optional, for private repos)

#### Methods

**`run_all() -> Dict[str, Any]`**
- Executes the complete integration workflow including:
  - Risk identification and analysis
  - Risk summary generation
  - Changelog generation
  - Release notes generation

**Returns:**
```json
{
  "risks": "Risk analysis results",
  "risk_summary": "Summary of identified risks",
  "changelog": "Generated changelog",
  "release_notes": "Generated release notes"
}
```

#### Dependencies

**Internal Dependencies:**
- `GitHubIntegration` from `autoprojectmanagement.services.integration_services.github_integration`
- `RiskManagement` from `autoprojectmanagement.main_modules.communication_risk.risk_management`
- `DocumentationAutomation` from `autoprojectmanagement.services.configuration_cli.documentation_automation`

**External Dependencies:**
- Python 3.8+
- GitHub API access
- Required packages from requirements.txt

#### Response Format

**Success Response:**
```json
{
  "risks": {
    "identified_risks": [
      {
        "risk_id": "risk-001",
        "category": "communication",
        "severity": "high",
        "description": "Lack of regular status updates",
        "mitigation": "Implement weekly status meetings"
      }
    ],
    "total_risks": 5,
    "high_severity_count": 2,
