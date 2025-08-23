# API Documentation Template

*Last updated: 2025-08-14*

This template provides a standardized format for documenting API endpoints in the AutoProjectManagement system. Use this template to ensure consistency across all API documentation.

## Endpoint Documentation Template

```markdown
### [Endpoint Name]

- **Method:** [HTTP Method: GET, POST, PUT, DELETE]
- **Path:** `/api/v1/[endpoint/path]`
- **Description:** [Brief description of what the endpoint does]
- **Authentication:** [Required/Optional]
- **Rate Limit:** [Requests per minute]

#### Parameters

**Path Parameters:**
- `[param_name]` ([data type], required/optional): [Description]

**Query Parameters:**
- `[param_name]` ([data type], required/optional, default=[value]): [Description]

**Request Body:**
```json
{
  "[field1]": "[data type] - [description]",
  "[field2]": "[data type] - [description]"
}
```

#### Response

**Success Response (200 OK):**
```json
{
  "[field1]": "[data type] - [description]",
  "[field2]": "[data type] - [description]"
}
```

**Error Responses:**
- `400 Bad Request`: [Error description]
- `404 Not Found`: [Error description]
- `500 Internal Server Error`: [Error description]

#### Example Request

```bash
curl -X [METHOD] "http://localhost:8000/api/v1/[endpoint]" \
  -H "Content-Type: application/json" \
  -d '{
    "[field1]": "[value1]",
    "[field2]": "[value2]"
  }'
```

#### Example Response

```json
{
  "[field1]": "[example_value1]",
  "[field2]": "[example_value2]",
  "timestamp": "2025-08-14T10:30:00.000Z"
}
```

#### Notes
- [Any additional notes, limitations, or considerations]
- [Dependencies or prerequisites]
- [Performance considerations]
```

## Model Documentation Template

```markdown
### [ModelName]

**Description:** [Brief description of the model]

**Fields:**
- `field_name` ([data type], required/optional): [Description with constraints]
- `field_name` ([data type], required/optional): [Description with constraints]

**Example:**
```json
{
  "field_name": "example_value",
  "field_name": 123
}
```

**Validation Rules:**
- [Rule 1: e.g., "Must be between 1-100 characters"]
- [Rule 2: e.g., "Must be a valid email format"]
```

## Error Documentation Template

```markdown
### [Error Code/Type]

**HTTP Status:** [Status code]
**Error Code:** [Internal error code if applicable]

**Description:** [Detailed description of when this error occurs]

**Response Format:**
```json
{
  "error": "[Error message]",
  "detail": "[Additional details]",
  "timestamp": "2025-08-14T10:30:00.000Z",
  "error_code": "[Internal error code]"
}
```

**Common Causes:**
1. [Cause 1]
2. [Cause 2]
3. [Cause 3]

**Resolution:**
- [Step 1 to resolve]
- [Step 2 to resolve]
- [Contact information if needed]
```

## Real-time Event Documentation Template

```markdown
### [Event Type]

**Event Type:** `[event_type_name]`
**Description:** [Description of what this event represents]

**Event Data Structure:**
```json
{
  "type": "[event_type]",
  "data": {
    "[field1]": "[data type] - [description]",
    "[field2]": "[data type] - [description]"
  },
  "timestamp": "2025-08-14T10:30:00.000Z",
  "event_id": "unique-event-identifier"
}
```

**When Published:**
- [Scenario 1 when this event is published]
- [Scenario 2 when this event is published]

**Subscribers:**
- [Component 1 that subscribes to this event]
- [Component 2 that subscribes to this event]
```

## Documentation Standards

### Naming Conventions
- **Endpoints**: Use kebab-case for paths (`/api/v1/project-status`)
- **Parameters**: Use snake_case for parameter names (`project_id`)
- **Models**: Use PascalCase for model names (`ProjectStatus`)
- **Fields**: Use snake_case for field names (`total_tasks`)

### Required Sections
Every endpoint documentation must include:
1. HTTP Method and Path
2. Description
3. Parameters (if any)
4. Request Body (if applicable)
5. Response format
6. Error responses
7. Example request and response
8. Notes and considerations

### Versioning
- Include API version in path (`/api/v1/`)
- Document breaking changes between versions
- Maintain backward compatibility when possible

### Examples
- Provide realistic example values
- Include both request and response examples
- Show error examples for common failure scenarios

### Language and Tone
- Use clear, concise language
- Avoid technical jargon when possible
- Be consistent in terminology
- Use active voice

## Review Checklist

Before publishing API documentation, verify:

- [ ] All endpoints are documented
- [ ] Examples are accurate and working
- [ ] Error responses are comprehensive
- [ ] Authentication requirements are specified
- [ ] Rate limits are documented
- [ ] Version information is included
- [ ] Cross-references to related endpoints
- [ ] Consistency with actual implementation

## Maintenance

- Update documentation when API changes
- Review documentation quarterly
- Verify examples against current implementation
- Remove deprecated endpoints
- Add migration guides for breaking changes

---

*This template is maintained by the AutoProjectManagement documentation team.*
*Last reviewed: 2025-08-14*
