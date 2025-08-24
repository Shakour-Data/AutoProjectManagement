# مستندات ماژول CLI Docker

## بررسی کلی
ماژول `cli_docker.py` یک رابط خط فرمان برای مدیریت محیط‌های Docker در سیستم AutoProjectManagement فراهم می‌کند. این ماژول به کاربران امکان می‌دهد تا سرویس‌های Docker را راه‌اندازی، شروع، متوقف و وضعیت آن‌ها را بررسی کنند، همچنین ابزارهای CLI Docker را نصب کنند.

## معماری

### ساختار دستورات
```mermaid
classDiagram
    class DockerCLI {
        +docker_cli(): None
        +setup(env: Optional[str], auto: bool): None
        +start(env: Optional[str]): None
        +stop(env: Optional[str]): None
