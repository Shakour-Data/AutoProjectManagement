# مستندات ماژول CLI

## بررسی کلی
ماژول `cli.py` به عنوان رابط خط فرمان اصلی برای سیستم AutoProjectManagement عمل می‌کند. این ماژول مجموعه‌ای جامع از دستورات برای مقداردهی اولیه پروژه، مدیریت وظایف، ردیابی پیشرفت و مدیریت سیستم با استفاده از چارچوب Click فراهم می‌کند.

## معماری

### ساختار دستورات
```mermaid
classDiagram
    class MainCLI {
        +main(): None
        +init(config, verbose): None
        +create_project(project_name, description, template): None
        +status(project_id, format): None
        +add_task(project_id, task_name, priority, description, assignee, due_date): None
        +report(project_id, report_type, output, format): None
        +update_task_status(project_id, task_id, new_status): None
        +help_command(list_commands, help_flag): None
    }
```

### جریان دستورات
```mermaid
flowchart TD
    A[گروه دستورات main] --> B[init]
