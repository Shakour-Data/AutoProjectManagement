# چک‌لیست بررسی کیفیت کد AutoProjectManagement

## 🎯 هدف
بررسی تمام فایل‌های کد برای:
- ✅ هماهنگی با سایر ماژول‌ها
- ✅ داک‌استرینگ کامل
- ✅ کامنت خط به خط
- ✅ استانداردهای کدنویسی تمیز

---

## 📋 چک‌لیست کلی

### 1. ساختار و سازماندهی پروژه
- [ ] بررسی ساختار پوشه‌ها و ماژول‌ها
- [ ] بررسی فایل‌های __init__.py در هر پوشه
- [ ] بررسی واردات (imports) و وابستگی‌ها

### 2. استانداردهای کدنویسی
- [ ] رعایت PEP 8
- [ ] نام‌گذاری متغیرها و توابع (snake_case)
- [ ] نام‌گذاری کلاس‌ها (PascalCase)
- [ ] حداکثر طول خط 79 کاراکتر
- [ ] استفاده از type hints

### 3. مستندسازی
- [ ] داک‌استرینگ برای تمام کلاس‌ها
- [ ] داک‌استرینگ برای تمام توابع و متدها
- [ ] کامنت‌گذاری منطق پیچیده
- [ ] README فایل‌ها برای ماژول‌های اصلی

### 4. هماهنگی ماژول‌ها
- [ ] بررسی وابستگی‌های بین ماژول‌ها
- [ ] بررسی چرخه‌های وابستگی (circular imports)
- [ ] بررسی رابط‌های API بین ماژول‌ها
- [ ] بررسی سازگاری ورژن‌ها

---

## 📁 فایل‌های اصلی - چک‌لیست اختصاصی

### 🔧 فایل‌های Core
- [ ] `__init__.py`
- [ ] `auto_runner.py`
- [ ] `cli.py`
- [ ] `migrate_reorganization.py`
- [ ] `setup_auto_environment.py`
- [ ] `vscode_extension.py`

### 🌐 API Layer
- [ ] `api/main.py`
- [ ] `api/services.py`

### 📊 ماژول‌های اصلی

#### 🎯 سیستم مدیریت پروژه
- [ ] `main_modules/project_management_system.py`

#### 💬 مدیریت ارتباطات و ریسک
- [ ] `main_modules/communication_risk/communication_management.py`
- [ ] `main_modules/communication_risk/communication_risk_doc_integration.py`
- [ ] `main_modules/communication_risk/risk_management.py`

#### 📊 جمع‌آوری و پردازش داده
- [ ] `main_modules/data_collection_processing/db_data_collector.py`
- [ ] `main_modules/data_collection_processing/input_handler.py`
- [ ] `main_modules/data_collection_processing/progress_data_generator.py`
- [ ] `main_modules/data_collection_processing/workflow_data_collector.py`

#### 📅 برنامه‌ریزی و تخمین
- [ ] `main_modules/planning_estimation/estimation_management.py`
- [ ] `main_modules/planning_estimation/gantt_chart_data.py`
- [ ] `main_modules/planning_estimation/scheduler.py`
- [ ] `main_modules/planning_estimation/scope_management.py`
- [ ] `main_modules/planning_estimation/wbs_aggregator.py`
- [ ] `main_modules/planning_estimation/wbs_merger.py`
- [ ] `main_modules/planning_estimation/wbs_parser.py`

#### 📈 گزارش پیشرفت
- [ ] `main_modules/progress_reporting/check_progress_dashboard_update.py`
- [ ] `main_modules/progress_reporting/dashboards_reports.py`
- [ ] `main_modules/progress_reporting/progress_calculator.py`
- [ ] `main_modules/progress_reporting/progress_report.py`
- [ ] `main_modules/progress_reporting/reporting.py`

#### 🔒 مدیریت کیفیت و کامیت
- [ ] `main_modules/quality_commit_management/commit_progress_manager.py`
- [ ] `main_modules/quality_commit_management/git_progress_updater.py`
- [ ] `main_modules/quality_commit_management/github_actions_automation.py`
- [ ] `main_modules/quality_commit_management/quality_management.py`

#### 👥 مدیریت منابع
- [ ] `main_modules/resource_management/resource_allocation_manager.py`
- [ ] `main_modules/resource_management/resource_leveling.py`
- [ ] `main_modules/resource_management/resource_management.py`

#### ✅ مدیریت تسک و گردش کار
- [ ] `main_modules/task_workflow_management/do_important_tasks.py`
- [ ] `main_modules/task_workflow_management/do_urgent_tasks.py`
- [ ] `main_modules/task_workflow_management/importance_urgency_calculator.py`
- [ ] `main_modules/task_workflow_management/task_executor.py`
- [ ] `main_modules/task_workflow_management/task_management_integration.py`
- [ ] `main_modules/task_workflow_management/task_management.py`

#### 🛠 ماژول‌های کمکی
- [ ] `main_modules/utility_modules/feature_weights.py`
- [ ] `main_modules/utility_modules/project_views_generator.py`
- [ ] `main_modules/utility_modules/setup_automation.py`
- [ ] `main_modules/utility_modules/setup_initialization.py`
- [ ] `main_modules/utility_modules/time_management.py`

### 🔧 سرویس‌ها

#### 🤖 سرویس‌های اتوماسیون
- [ ] `services/automation_services/auto_commit.py`
- [ ] `services/automation_services/backup_manager.py`

#### ⚙️ پیکربندی CLI
- [ ] `services/configuration_cli/cli_commands.py`
- [ ] `services/configuration_cli/config_and_token_management.py`
- [ ] `services/configuration_cli/json_data_linker.py`

#### 🔗 سرویس‌های یکپارچه‌سازی
- [ ] `services/integration_services/github_integration.py`
- [ ] `services/integration_services/github_project_manager.py`
- [ ] `services/integration_services/integration_manager.py`
- [ ] `services/integration_services/vscode_extension_installer.py`
- [ ] `services/integration_services/wiki_git_operations.py`
- [ ] `services/integration_services/wiki_page_mapper.py`
- [ ] `services/integration_services/wiki_sync_service.py`

### 📋 قالب‌ها
- [ ] `templates/documentation_standard.py`
- [ ] `templates/header_updater.py`
- [ ] `templates/standard_header.py`

---

## 🔍 معیارهای بررسی دقیق

### 1. داک‌استرینگ استاندارد
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    خلاصه عملکرد تابع در یک خط.
    
    Args:
        param1: توضیح پارامتر اول
        param2: توضیح پارامتر دوم
    
    Returns:
        توضیح مقدار بازگشتی
    
    Raises:
        ExceptionType: توضیح شرایط خطا
    
    Example:
        >>> function_name(value1, value2)
        expected_result
    """
```

### 2. کامنت‌گذاری
- [ ] کامنت برای هر کلاس و توابع پیچیده
- [ ] کامنت برای منطق‌های پیچیده
- [ ] کامنت برای magic numbers
- [ ] کامنت برای workaroundها

### 3. تمیزی کد
- [ ] حذف importهای unused
- [ ] استفاده از f-strings به جای format
- [ ] استفاده از list/dict comprehensions
- [ ] حذف کدهای تکراری (DRY principle)
- [ ] استفاده از context managers برای file handling

### 4. هماهنگی ماژول‌ها
- [ ] بررسی importها در هر فایل
- [ ] بررسی وابستگی‌های متقابل
- [ ] بررسی استفاده از اینترفیس‌ها
- [ ] بررسی تست‌های واحد برای ماژول‌ها

---

## 📊 وضعیت پیشرفت

| دسته | تعداد فایل‌ها | بررسی شده | درصد پیشرفت |
|------|----------------|-----------|-------------|
| Core Files | 6 | 1 | 17% |
| API Layer | 2 | 0 | 0% |
| Main Modules | 35 | 0 | 0% |
| Services | 11 | 1 | 9% |
| Templates | 3 | 0 | 0% |
| **کل** | **57** | **2** | **4%** |

---

## 📝 نکات اجرایی

### ابزارهای مورد نیاز:
- [ ] flake8 برای بررسی سبک کد
- [ ] black برای فرمت‌دهی خودکار
- [ ] mypy برای type checking
- [ ] pydocstyle برای بررسی داک‌استرینگ

### دستورات اجرایی:
```bash
# بررسی سبک کد
flake8 autoprojectmanagement/ --max-line-length=79

# فرمت‌دهی خودکار
black autoprojectmanagement/ --line-length=79

# بررسی type hints
mypy autoprojectmanagement/ --ignore-missing-imports

# بررسی داک‌استرینگ
pydocstyle autoprojectmanagement/
```

---

## ✅ نحوه استفاده از چک‌لیست

1. **برای هر فایل** موارد زیر را بررسی کنید:
   - [ ] داک‌استرینگ کامل برای کلاس‌ها و توابع
   - [ ] کامنت‌گذاری منطق پیچیده
   - [ ] رعایت استاندارد PEP 8
   - [ ] استفاده از type hints
   - [ ] بررسی هماهنگی با ماژول‌های دیگر

2. **پس از بررسی هر فایل**:
   - تیک مربوطه را بزنید ✅
   - مشکلات را در ستون "یادداشت‌ها" ثبت کنید
   - تاریخ بررسی را ثبت کنید

3. **برای ماژول‌های وابسته**:
   - بررسی کنید که تغییرات در یک ماژول بر ماژول‌های دیگر تأثیر نگذارد
   - تست‌های واحد را اجرا کنید

---

## 📅 تاریخچه بررسی‌ها

| تاریخ | فایل‌های بررسی شده | توسط | یادداشت‌ها |
|-------|-------------------|------|-------------|
| 2024-12-19 | `auto_runner.py`, `auto_commit.py` | BLACKBOXAI | بررسی اولیه انجام شد - مشکلات شناسایی شده در گزارش زیر |

---

## 📋 گزارش تحلیل اولیه

### ✅ نقاط قوت شناسایی شده:
1. **ساختار منظم**: فایل‌ها به‌خوبی سازماندهی شده‌اند
2. **داک‌استرینگ مناسب**: کلاس‌ها و توابع اصلی دارای داک‌استرینگ هستند
3. **ماژولار بودن**: کد به‌خوبی به ماژول‌های مجزا تقسیم شده است

### ❌ مشکلات شناسایی شده:

#### در `auto_runner.py`:
- [ ] **نیاز به type hints**: برخی توابع فاقد type hints کامل هستند
- [ ] **کامنت‌گذاری ناکافی**: برخی منطق‌های پیچیده نیاز به کامنت بیشتر دارند
- [ ] **خطوط طولانی**: برخی خطوط بیش از 79 کاراکتر هستند
- [ ] **Magic numbers**: اعداد سخت‌کد شده مانند 300، 600، 3600 نیاز به توضیح دارند

#### در `auto_commit.py`:
- [ ] **Importهای پیچیده**: استفاده از importlib برای import پویا نیاز به توضیح دارد
- [ ] **تابع بسیار بزرگ**: تابع `commit_and_push` بیش از حد بزرگ است
- [ ] **کامنت‌گذاری ناکافی**: برخی منطق‌های پیچیده کامنت ندارند
- [ ] **Magic strings**: استفاده از stringهای سخت‌کد شده برای مسیر فایل‌ها
- [ ] **Error handling**: برخی جاها error handling کامل نیست

### 🔧 پیشنهادات بهبود:
1. **ایجاد فایل constants.py** برای magic numbers و strings
2. **تقسیم توابع بزرگ به توابع کوچکتر**
3. **اضافه کردن type hints کامل**
4. **بهبود error handling با try-except blocks**
5. **اضافه کردن unit tests برای ماژول‌های کلیدی**

---

## 🔄 به‌روزرسانی
این چک‌لیست باید به‌صورت مداوم به‌روزرسانی شود. پس از هر مرحله بررسی، تیک‌ها را بزنید و یادداشت‌های مربوطه را اضافه کنید.
