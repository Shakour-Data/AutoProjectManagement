# مستندات ماژول Setup Auto Environment

## بررسی کلی
ماژول `setup_auto_environment.py` عملکرد راه‌اندازی جامع برای ایجاد یک محیط کامل مدیریت پروژه خودکار فراهم می‌کند. این ماژول ایجاد ساختار دایرکتوری، تولید فایل پیکربندی، خودکارسازی اسکریپت، راه‌اندازی فضای کاری VS Code، مدیریت وابستگی و یکپارچه‌سازی Git را مدیریت می‌کند.

## معماری

### ساختار کلاس
```mermaid
classDiagram
    class AutoEnvironmentSetup {
        -project_path: str
        -extension_dir: str
        -logger: logging.Logger
        +__init__(project_path: Optional[str])
        +create_project_structure(): None
        +create_auto_config(): None
        +create_startup_script(): None
        +create_stop_script(): None
        +create_status_script(): None
        +create_vscode_workspace(): None
        +create_requirements_file(): None
        +create_gitignore(): None
        +install_dependencies(): None
        +setup_complete_environment(): None
        -_setup_logging(): logging.Logger
    }
```

## عملکرد تفصیلی

### کلاس AutoEnvironmentSetup

#### مقداردهی اولیه
**متد**: `__init__(project_path: Optional[str] = None)`

کلاس AutoEnvironmentSetup را با مسیر پروژه مقداردهی اولیه می‌کند و لاگ‌گیری را راه‌اندازی می‌کند.

**پارامترها**:
- `project_path`: مسیر اختیاری به دایرکتوری پروژه.

#### ایجاد ساختار پروژه
**متد**: `create_project_structure() -> None`

ساختار کامل پروژه را برای مدیریت خودکار ایجاد می‌کند، شامل دایرکتوری‌های لاگ، پیکربندی، داده، گزارش و پشتیبان.

#### ایجاد پیکربندی خودکار
**متد**: `create_auto_config() -> None`

یک فایل پیکربندی JSON با تمام تنظیمات لازم برای سیستم AutoProjectManagement تولید می‌کند.

#### ایجاد اسکریپت راه‌اندازی
**متد**: `create_startup_script() -> None`

یک اسکریپت شل برای راه‌اندازی سیستم مدیریت پروژه خودکار با لاگ‌گیری و مدیریت خطای مناسب ایجاد می‌کند.

#### ایجاد اسکریپت توقف
**متد**: `create_stop_script() -> None`

یک اسکریپت شل برای توقف گرانولار سیستم مدیریت پروژه خودکار و انجام پاکسازی ایجاد می‌کند.

#### ایجاد اسکریپت وضعیت
**متد**: `create_status_script() -> None`

یک اسکریپت شل برای نمایش وضعیت فعلی سیستم مدیریت پروژه خودکار ایجاد می‌کند.

#### ایجاد فضای کاری VS Code
**متد**: `create_vscode_workspace() -> None`

یک فایل فضای کاری VS Code با تنظیمات بهینه‌شده برای مدیریت پروژه خودکار ایجاد می‌کند.

#### ایجاد فایل Requirements
**متد**: `create_requirements_file() -> None`

یک فایل requirements.txt با تمام وابستگی‌های لازم برای سیستم AutoProjectManagement ایجاد می‌کند.

#### ایجاد Gitignore
**متد**: `create_gitignore() -> None`

یک فایل .gitignore با الگوها برای حذف فایل‌های موقت، لاگ‌ها، پشتیبان‌ها و سایر فایل‌های غیرضروری از کنترل نسخه ایجاد می‌کند.

#### نصب وابستگی‌ها
**متد**: `install_dependencies() -> None`

تمام بسته‌های Python لازم را از فایل requirements نصب می‌کند.

#### راه‌اندازی محیط کامل
**متد**: `setup_complete_environment() -> None`

فرآیند راه‌اندازی کامل را هماهنگ می‌کند شامل ایجاد دایرکتوری، تولید پیکربندی، ایجاد اسکریپت و نصب وابستگی.

### تابع اصلی
**تابع**: `main() -> None`

نقطه ورود اصلی برای اسکریپت راه‌اندازی، فراهم کردن رابط خط فرمان برای راه‌اندازی محیط مدیریت پروژه خودکار.

## مثال‌های استفاده

### راه‌اندازی پایه
```python
from autoprojectmanagement.setup_auto_environment import AutoEnvironmentSetup

# مقداردهی اولیه AutoEnvironmentSetup
setup = AutoEnvironmentSetup()

# راه‌اندازی محیط کامل
setup.setup_complete_environment()
```

### استفاده از خط فرمان
```bash
# راه‌اندازی در دایرکتوری فعلی
python -m autoprojectmanagement.setup_auto_environment

# راه‌اندازی در دایرکتوری خاص
python -m autoprojectmanagement.setup_auto_environment --path /path/to/project

# فعال کردن لاگ‌گیری تفصیلی
python -m autoprojectmanagement.setup_auto_environment --verbose
```

## فایل‌های پیکربندی ایجاد شده

### فایل پیکربندی خودکار
واقع در `.auto_project/config/auto_config.json`، این فایل شامل تنظیمات برای موارد زیر است:
- ویژگی‌های مدیریت خودکار
- پیکربندی‌های نظارت
- یکپارچه‌سازی Git
- تنظیمات گزارش‌دهی
- اعلان‌ها
- پیکربندی‌های پشتیبان

### فضای کاری VS Code
واقع در `auto_project_management.code-workspace`، این فایل شامل موارد زیر است:
- تنظیمات پوشه
- پیکربندی‌های ویرایشگر
- پیکربندی‌های راه‌اندازی برای دیباگ
- تعاریف وظایف برای خودکارسازی

### اسکریپت‌های شل
- `start_auto_management.sh`: سیستم مدیریت خودکار را راه‌اندازی می‌کند
- `stop_auto_management.sh`: سیستم مدیریت خودکار را متوقف می‌کند
- `status_auto_management.sh`: وضعیت سیستم را نمایش می‌دهد

## وابستگی‌ها
- **os**: برای تعاملات سیستم عامل
- **sys**: برای پارامترهای خاص سیستم
- **json**: برای مدیریت فایل‌های JSON
- **subprocess**: برای اجرای دستورات شل
- **shutil**: برای عملیات فایل
- **logging**: برای راه‌اندازی لاگ‌گیری
- **pathlib**: برای دستکاری مسیرها

## مدیریت خطا
- لاگ‌گیری خطای جامع برای تمام عملیات
