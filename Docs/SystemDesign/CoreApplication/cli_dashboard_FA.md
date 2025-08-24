# مستندات ماژول CLI Dashboard

## بررسی کلی
ماژول `cli_dashboard.py` یک رابط خط فرمان جامع برای مدیریت سیستم داشبورد AutoProjectManagement فراهم می‌کند. این ماژول به کاربران امکان می‌دهد تا داشبورد را از طریق دستورات CLI شهودی که با چارچوب Click ساخته شده‌اند، راه‌اندازی، متوقف، نظارت و پیکربندی کنند.

## معماری

### ساختار کلاس
```mermaid
classDiagram
    class DashboardCLI {
        -default_port: int = 3000
        -default_host: str = "127.0.0.1"
        -api_base_url: str
        +start_dashboard(port, host): bool
        +stop_dashboard(): bool
        +dashboard_status(): Dict[str, Any]
        +open_dashboard(): bool
        +export_dashboard_data(format, output_file): bool
        +show_dashboard_info(): None
        +create_custom_view(layout_name, widgets, refresh_rate, theme): bool
        +share_dashboard_view(layout_name, output_format): bool
