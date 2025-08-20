# نمودارهای جریان داده (DFD) - سیستم AutoProjectManagement

## مرور کلی
این سند نمودارهای جامع جریان داده را برای سیستم AutoProjectManagement ارائه می‌دهد که نشان می‌دهد داده‌ها چگونه از طریق اجزا و ماژول‌های مختلف بر اساس پیاده‌سازی واقعی حرکت می‌کنند.

## فهرست مطالب
۱. [نمودار زمینه (سطح ۰)](#نمودار-زمینه-سطح-۰)
۲. [سطح ۱ DFD - مرور کلی سیستم](#سطح-۱-dfd-مرور-کلی-سیستم)
۳. [سطح ۲ DFD - ماژول‌های اصلی](#سطح-۲-dfd-ماژول‌های-اصلی)
۴. [سطح ۳ DFD - جریان‌های دقیق ماژول](#سطح-۳-dfd-جریان‌های-دقیق-ماژول)
۵. [ذخیره‌گاه‌های داده](#ذخیره-گاه‌های-داده)
۶. [توصیف جریان‌های داده](#توصیف-جریان‌های-داده)

---

## نمودار زمینه (سطح ۰)

```mermaid
graph TD
    Developer[/"توسعه‌دهنده/مدیر پروژه"/]
    System[/"سیستم AutoProjectManagement"/]
    GitHub[/"مخزن GitHub"/]
    VSCode[/"افزونه VSCode"/]
    Wiki[/"مستندات Wiki"/]
    Backup[/"سیستم پشتیبان‌گیری"/]
    
    Developer -->|ورودی وظیفه و دستورات| System
    System -->|گزارش پیشرفت و وضعیت| Developer
    System <-->|Push/Pull کامیت‌ها| GitHub
    System <-->|بروزرسانی‌های لحظه‌ای| VSCode
    System <-->|همگام‌سازی مستندات| Wiki
    System -->|داده‌های پشتیبان| Backup
    
    style System fill:#f9f,stroke:#333,stroke-width:4px
```

---

## سطح ۱ DFD - مرور کلی سیستم

### فرآیندهای اصلی
| شناسه فرآیند | نام فرآیند | توضیحات |
|------------|--------------|-------------|
| P1 | **رابط CLI** | رابط خط فرمان برای تعامل کاربر |
| P2 | **هسته مدیریت پروژه** | هماهنگ‌کننده مرکزی که تمام فعالیت‌های پروژه را مدیریت می‌کند |
| P3 | **جمع‌آوری و پردازش داده** | جمع‌آوری و پردازش داده‌های پروژه از منابع مختلف |
| P4 | **برنامه‌ریزی و برآورد** | ایجاد برنامه‌های پروژه، زمان‌بندی و برآوردها |
| P5 | **مدیریت وظیفه و گردش کار** | مدیریت اجرای وظایف و اتوماسیون گردش کار |
| P6 | **گزارش‌دهی پیشرفت** | تولید گزارش‌های پیشرفت و داشبوردها |
| P7 | **مدیریت کیفیت و کامیت** | مدیریت کیفیت کد و کامیت‌های خودکار |
| P8 | **مدیریت منابع** | مدیریت تخصیص منابع و تراز منابع |
| P9 | **ارتباط و ریسک** | مدیریت ارتباطات و ریسک |
| P10 | **پشتیبان‌گیری و بازیابی** | مدیریت پشتیبان‌گیری و بازیابی سیستم |

```mermaid
graph TD
    User[/"کاربر"/]
    
    P1[("رابط CLI")]
    P2[("هسته مدیریت پروژه")]
    P3[("جمع‌آوری و پردازش داده")]
    P4[("برنامه‌ریزی و برآورد")]
    P5[("مدیریت وظیفه و گردش کار")]
    P6[("گزارش‌دهی پیشرفت")]
    P7[("مدیریت کیفیت و کامیت")]
    P8[("مدیریت منابع")]
    P9[("ارتباط و ریسک")]
    P10[("پشتیبان‌گیری و بازیابی")]
    
    DS1[(پایگاه داده وظایف)]
    DS2[(پایگاه داده پیشرفت)]
    DS3[(پایگاه داده پیکربندی)]
    DS4[(تاریخچه کامیت)]
    DS5[(ذخیره‌گاه پشتیبان)]
    
    User -->|دستورات CLI| P1
    P1 --> P2
    P2 --> P3
    P2 --> P4
    P2 --> P5
    P2 --> P6
    P2 --> P7
    P2 --> P8
    P2 --> P9
    P2 --> P10
    
    P3 --> DS1
    P4 --> DS1
    P5 --> DS2
    P6 --> DS2
    P7 --> DS4
    P8 --> DS1
    P9 --> DS2
    P10 --> DS5
```

---

## سطح ۲ DFD - ماژول‌های اصلی

### ۲.۱ - جمع‌آوری و پردازش داده
```mermaid
graph TD
    subgraph "جمع‌آوری و پردازش داده"
        Input_Handler[("پردازشگر ورودی")]
        Workflow_Collector[("جمع‌آورنده داده گردش کار")]
        Progress_Generator[("تولیدکننده داده پیشرفت")]
        
        Raw_Input[(ورودی خام)]
        Processed_Data[(داده پردازش شده)]
        Progress_Data[(داده پیشرفت)]
        
        CLI_Input[/"ورودی CLI"/] --> Input_Handler
        JSON_Input[/"فایل‌های JSON"/] --> Input_Handler
        Git_Data[/"داده Git"/] --> Workflow_Collector
        
        Input_Handler --> Raw_Input
        Workflow_Collector --> Processed_Data
        Raw_Input --> Progress_Generator
        Processed_Data --> Progress_Generator
        Progress_Generator --> Progress_Data
    end
```

### ۲.۲ - مدیریت وظیفه و گردش کار
```mermaid
graph TD
    subgraph "مدیریت وظیفه و گردش کار"
        Task_Management[("مدیریت وظیفه")]
        Importance_Calc[("ماشین حساب اهمیت")]
        Urgency_Calc[("ماشین حساب فوریت")]
        Task_Executor[("اجرا کننده وظیفه")]
        
        Task_Queue[(صف وظیفه)]
        Priority_Data[(داده اولویت)]
        
        Scheduled_Tasks[/"وظایف زمان‌بندی شده"/] --> Task_Management
        Task_Management --> Importance_Calc
        Task_Management --> Urgency_Calc
        Importance_Calc --> Priority_Data
        Urgency_Calc --> Priority_Data
        Priority_Data --> Task_Executor
        Task_Executor --> Task_Queue
    end
```

### ۲.۳ - اتوماسیون Git و مدیریت کامیت
```mermaid
graph TD
    subgraph "اتوماسیون Git و مدیریت کامیت"
        Commit_Manager[("مدیر کامیت")]
        Message_Generator[("تولیدکننده پیام کامیت")]
        Quality_Checker[("بررسی‌کننده کیفیت")]
        Git_Progress[("بروزرسان پیشرفت Git")]
        
        Ready_Commits[(کامیت‌های آماده)]
        Git_History[(تاریخچه Git)]
        
        Completed_Tasks[/"وظایف تکمیل شده"/] --> Commit_Manager
        Commit_Manager --> Quality_Checker
        Quality_Checker -->|تایید/رد| Commit_Manager
        Commit_Manager --> Message_Generator
        Message_Generator --> Git_Progress
        Git_Progress --> Git_History
        Git_Progress -->|"Push به GitHub"| GitHub[/"GitHub"/]
    end
```

---

## سطح ۳ DFD - جریان‌های دقیق ماژول

### ۳.۱ - گزارش‌دهی پیشرفت
```mermaid
graph TD
    subgraph "گزارش‌دهی پیشرفت"
        Data_Aggregator[("جمع‌آورنده داده")]
        Progress_Analyzer[("تحلیل‌گر پیشرفت")]
        Report_Formatter[("قالب‌بند گزارش")]
        
        Progress_Data[(داده پیشرفت)]
        Reports[(گزارش‌ها)]
        
        Task_Progress[/"پیشرفت وظیفه"/] --> Data_Aggregator
        Commit_Data[/"داده کامیت"/] --> Data_Aggregator
        Data_Aggregator --> Progress_Data
        Progress_Data --> Progress_Analyzer
        Progress_Analyzer --> Report_Formatter
        Report_Formatter --> Reports
        Reports -->|"progress_report.md"| User[/"کاربر"/]
    end
```

### ۳.۲ - مدیریت منابع
```mermaid
graph TD
    subgraph "مدیریت منابع"
        Resource_Allocator[("تخصیص‌دهنده منابع")]
        Resource_Leveling[("تراز منابع")]
        
        Resource_Requests[(درخواست‌های منابع)]
        Allocated_Resources[(منابع تخصیص یافته)]
        
        Task_Requirements[/"نیازمندی‌های وظیفه"/] --> Resource_Allocator
        Resource_Availability[/"در دسترس بودن منابع"/] --> Resource_Allocator
        Resource_Allocator --> Resource_Requests
        Resource_Requests --> Resource_Leveling
        Resource_Leveling --> Allocated_Resources
    end
```

---

## ذخیره‌گاه‌های داده

### ذخیره‌گاه‌های داده اصلی
| ذخیره‌گاه داده | محل | توضیحات | قالب |
|------------|----------|-------------|---------|
| **پایگاه داده وظایف** | `JSonDataBase/Inputs/UserInputs/` | وظایف و پیکربندی‌های تعریف شده توسط کاربر | JSON |
| **پایگاه داده پیشرفت** | `JSonDataBase/OutPuts/` | داده‌های پیشرفت محاسبه شده و وضعیت | JSON |
| **پایگاه داده پیکربندی** | `autoproject_configuration.py` | پارامترهای پیکربندی سیستم | Python |
| **تاریخچه کامیت** | `.git/` directory | تاریخچه کامیت Git و متاداده | Git |
| **ذخیره‌گاه پشتیبان** | `backups/` | پشتیبان‌ها و آرشیوهای سیستم | ZIP/JSON |

### طرح‌های ذخیره‌گاه داده

#### طرح پایگاه داده وظایف
```json
{
  "task_id": "string",
  "task_name": "string",
  "description": "string",
  "priority": "integer",
  "urgency": "integer",
  "importance": "integer",
  "estimated_hours": "float",
  "actual_hours": "float",
  "status": "string",
  "dependencies": ["task_id"],
  "assigned_resources": ["resource_id"],
  "due_date": "date"
}
```

#### طرح پایگاه داده پیشرفت
```json
{
  "progress_id": "string",
  "task_id": "string",
  "completion_percentage": "float",
  "hours_spent": "float",
  "status": "string",
  "last_updated": "datetime"
}
```

---

## توصیف جریان‌های داده

### جریان‌های داده اصلی

| شناسه جریان | نام جریان | منبع | مقصد | عناصر داده | فرکانس |
|---------|-----------|--------|-------------|---------------|-----------|
| F1 | ورودی وظیفه | رابط CLI | مدیریت وظیفه | داده خام وظیفه، دستورات | در صورت نیاز |
| F2 | وظایف معتبر | اعتبارسنج وظیفه | تجزیه‌گر WBS | اشیاء وظیفه معتبر | در زمان واقعی |
| F3 | ساختار WBS | تجزیه‌گر WBS | زمان‌بند | ساختار سلسله‌مراتبی وظیفه | در ایجاد وظیفه |
| F4 | بروزرسانی پیشرفت | اجرا کننده وظیفه | گزارش‌دهی پیشرفت | داده تکمیل وظیفه | مداوم |
| F5 | داده کامیت | مدیر کامیت | تاریخچه Git | اطلاعات کامیت | در تکمیل وظیفه |
| F6 | درخواست پشتیبان | نمایشگر سیستم | مدیر پشتیبان | ماشه پشتیبان‌گیری | زمان‌بندی شده |
| F7 | تخصیص منابع | تخصیص‌دهنده منابع | سیستم وظیفه | تخصیص‌های منابع | در زمان‌بندی وظیفه |

### نگاشت پیاده‌سازی
- **رابط CLI**: `autoprojectmanagement/cli.py`
- **هسته مدیریت پروژه**: `autoprojectmanagement/main_modules/project_management_system.py`
- **جمع‌آوری داده**: `autoprojectmanagement/main_modules/data_collection_processing/`
- **مدیریت وظیفه**: `autoprojectmanagement/main_modules/task_workflow_management/`
- **گزارش‌دهی پیشرفت**: `autoprojectmanagement/main_modules/progress_reporting/`
- **مدیریت کیفیت**: `autoprojectmanagement/main_modules/quality_commit_management/`
- **مدیریت منابع**: `autoprojectmanagement/main_modules/resource_management/`
- **سیستم پشتیبان‌گیری**: `autoprojectmanagement/services/automation_services/backup_manager.py`

---

این سند یک نمایش کامل و دقیق از جریان داده سیستم AutoProjectManagement بر اساس پیاده‌سازی واقعی ارائه می‌دهد.
