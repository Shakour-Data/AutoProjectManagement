# مستندات ماژول Docker Setup

## بررسی کلی
ماژول `docker_setup.py` عملکرد راه‌اندازی و مدیریت خودکار Docker را برای سیستم AutoProjectManagement فراهم می‌کند. این ماژول نصب Docker، تشخیص محیط، مدیریت سرویس و راه‌اندازی پس از نصب را مدیریت می‌کند.

## معماری

### ساختار کلاس
```mermaid
classDiagram
    class DockerSetup {
        -project_root: Path
        -script_path: Path
        +__init__(project_root: Optional[str])
        +check_docker_installed(): bool
        +check_docker_compose(): bool
        +detect_environment(): str
        +setup_docker(environment: Optional[str], auto: bool): bool
        +get_compose_file(environment: str): str
        +start_services(environment: Optional[str]): bool
        +stop_services(environment: Optional[str]): bool
        +show_status(environment: Optional[str]): None
        +install_docker_cli(): bool
    }
```

## عملکرد تفصیلی

### کلاس DockerSetup

#### مقداردهی اولیه
**متد**: `__init__(project_root: Optional[str] = None)`

