"""
path: wiki_sync_service.py
File: wiki_sync_service.py
Purpose: Service for synchronizing project documentation with external wiki systems
Author: AutoProjectManagement System
Version: 1.0.0
License: MIT
Description: Provides comprehensive wiki synchronization capabilities including content validation,
             conflict resolution, automated syncing, and integration with project management workflows.
"""

import os
import json
import hashlib
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import requests
from dataclasses import dataclass, asdict
from enum import Enum

# Phase 1: Foundation & Core Architecture
# =====================================

class SyncStatus(Enum):
    """Enumeration for synchronization status tracking"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CONFLICT = "conflict"

@dataclass
class WikiPage:
    """Data class representing a wiki page structure"""
    title: str
    content: str
    last_modified: datetime
    version: int
    checksum: str
    metadata: Dict[str, Any]

@dataclass
class SyncRecord:
    """Data class for tracking synchronization history"""
    page_title: str
    sync_time: datetime
    status: SyncStatus
    local_checksum: str
    remote_checksum: str
    changes_detected: bool
    error_message: Optional[str] = None

class WikiSyncConfig:
    """Configuration management for wiki synchronization service"""
    
    def __init__(self, config_path: str = "config/wiki_sync.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "wiki_api_url": "https://wiki.example.com/api.php",
            "username": "sync_bot",
            "password": "",
            "sync_interval": 3600,
            "retry_attempts": 3,
            "timeout": 30,
            "conflict_resolution": "manual",
            "excluded_patterns": ["*.tmp", "*.log"],
            "sync_directories": ["docs", "wiki"]
        }
    
    def _validate_config(self) -> None:
        """Validate configuration parameters"""
        required_keys = ["wiki_api_url", "username", "password"]
        for key in required_keys:
            if not self.config.get(key):
                raise ValueError(f"Missing required configuration: {key}")
    
    def save_config(self) -> None:
        """Save configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

class WikiAPIClient:
    """Client for interacting with wiki API"""
    
    def __init__(self, config: WikiSyncConfig):
        self.config = config
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
    
    def authenticate(self) -> bool:
        """Authenticate with wiki API"""
        try:
            login_data = {
                "action": "login",
                "lgname": self.config.config["username"],
                "lgpassword": self.config.config["password"],
                "format": "json"
            }
            
            response = self.session.post(
                self.config.config["wiki_api_url"],
                data=login_data,
                timeout=self.config.config["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("login", {}).get("result") == "Success"
            
            return False
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            return False
    
    def get_page_content(self, page_title: str) -> Optional[WikiPage]:
        """Retrieve page content from wiki"""
        try:
            params = {
                "action": "query",
                "prop": "revisions",
                "titles": page_title,
                "rvprop": "content|timestamp",
                "format": "json"
            }
            
            response = self.session.get(
                self.config.config["wiki_api_url"],
                params=params,
                timeout=self.config.config["timeout"]
            )
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                
                for page_id, page_data in pages.items():
                    if page_id != "-1":  # Page exists
                        revisions = page_data.get("revisions", [])
                        if revisions:
                            content = revisions[0].get("*", "")
                            timestamp = revisions[0].get("timestamp", "")
                            
                            return WikiPage(
                                title=page_title,
                                content=content,
                                last_modified=datetime.fromisoformat(timestamp.replace('Z', '+00:00')),
                                version=1,
                                checksum=self._calculate_checksum(content),
                                metadata={}
                            )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get page content: {str(e)}")
            return None
    
    def update_page(self, page: WikiPage) -> bool:
        """Update page content on wiki"""
        try:
            # Get edit token
            token_params = {
                "action": "query",
                "meta": "tokens",
                "type": "csrf",
                "format": "json"
            }
            
            token_response = self.session.get(
                self.config.config["wiki_api_url"],
                params=token_params
            )
            
            if token_response.status_code != 200:
                return False
            
            token = token_response.json().get("query", {}).get("tokens", {}).get("csrftoken")
            
            if not token:
                return False
            
            # Update page
            edit_data = {
                "action": "edit",
                "title": page.title,
                "text": page.content,
                "token": token,
                "format": "json",
                "summary": f"Auto-sync: {datetime.now(timezone.utc).isoformat()}"
            }
            
            response = self.session.post(
                self.config.config["wiki_api_url"],
                data=edit_data,
                timeout=self.config.config["timeout"]
            )
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Failed to update page: {str(e)}")
            return False
    
    def _calculate_checksum(self, content: str) -> str:
        """Calculate MD5 checksum for content"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()

# Phase 2: Enhanced Features & Validation
# =======================================

class ContentValidator:
    """Validates wiki content for consistency and standards"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_content(self, content: str) -> Tuple[bool, List[str]]:
        """Validate content against wiki standards"""
        issues = []
        
        # Check for empty content
        if not content.strip():
            issues.append("Content is empty")
            return False, issues
        
        # Check for proper markdown structure
        if not self._has_proper_headers(content):
            issues.append("Missing proper header structure")
        
        # Check for broken links
        broken_links = self._find_broken_links(content)
        if broken_links:
            issues.extend([f"Broken link: {link}" for link in broken_links])
        
        # Check for formatting issues
        if not self._has_consistent_formatting(content):
            issues.append("Inconsistent formatting detected")
        
        return len(issues) == 0, issues
    
    def _has_proper_headers(self, content: str) -> bool:
        """Check if content has proper header structure"""
        lines = content.split('\n')
        has_h1 = any(line.startswith('# ') for line in lines)
        has_h2 = any(line.startswith('## ') for line in lines)
        return has_h1 and has_h2
    
    def _find_broken_links(self, content: str) -> List[str]:
        """Find broken markdown links"""
        import re
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        broken_links = []
        for text, url in links:
            if url.startswith('http') and not self._is_valid_url(url):
                broken_links.append(url)
        
        return broken_links
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code < 400
        except:
            return False
    
    def _has_consistent_formatting(self, content: str) -> bool:
        """Check for consistent formatting"""
        # Simple check for consistent bullet points
        lines = content.split('\n')
        bullet_styles = set()
        
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                bullet_styles.add('dash')
            elif line.startswith('* '):
                bullet_styles.add('asterisk')
            elif line.startswith('+ '):
                bullet_styles.add('plus')
        
        return len(bullet_styles) <= 1

class ConflictResolver:
    """Handles conflicts between local and remote wiki content"""
    
    def __init__(self, resolution_strategy: str = "manual"):
        self.resolution_strategy = resolution_strategy
        self.logger = logging.getLogger(__name__)
    
    def resolve_conflict(self, local_page: WikiPage, remote_page: WikiPage) -> WikiPage:
        """Resolve conflicts between local and remote content"""
        if self.resolution_strategy == "local_wins":
            return local_page
        elif self.resolution_strategy == "remote_wins":
            return remote_page
        elif self.resolution_strategy == "timestamp":
            return local_page if local_page.last_modified > remote_page.last_modified else remote_page
        else:  # manual
            return self._create_merge_page(local_page, remote_page)
    
    def _create_merge_page(self, local_page: WikiPage, remote_page: WikiPage) -> WikiPage:
        """Create merged content from local and remote pages"""
        merged_content = f"""# Merged Content - Manual Review Required

## Local Version (Last Modified: {local_page.last_modified})
{local_page.content}

## Remote Version (Last Modified: {remote_page.last_modified})
{remote_page.content}

## Resolution Notes
Please review both versions and resolve conflicts manually.
"""
        
        return WikiPage(
            title=local_page.title,
            content=merged_content,
            last_modified=datetime.now(timezone.utc),
            version=max(local_page.version, remote_page.version) + 1,
            checksum=hashlib.md5(merged_content.encode('utf-8')).hexdigest(),
            metadata={"conflict_resolution": "manual"}
        )

# Phase 3: Advanced Features & Integration
# ========================================

class SyncScheduler:
    """Manages scheduled synchronization tasks"""
    
    def __init__(self, sync_interval: int = 3600):
        self.sync_interval = sync_interval
        self.logger = logging.getLogger(__name__)
        self.scheduled_tasks = {}
    
    def schedule_sync(self, page_title: str, interval: Optional[int] = None) -> bool:
        """Schedule automatic sync for a page"""
        interval = interval or self.sync_interval
        self.scheduled_tasks[page_title] = {
            "interval": interval,
            "last_sync": None,
            "next_sync": datetime.now(timezone.utc)
        }
        return True
    
    def get_pending_syncs(self) -> List[str]:
        """Get list of pages ready for sync"""
        pending = []
        now = datetime.now(timezone.utc)
        
        for page_title, task_info in self.scheduled_tasks.items():
            next_sync = task_info.get("next_sync")
            if next_sync and next_sync <= now:
                pending.append(page_title)
        
        return pending
    
    def update_sync_time(self, page_title: str) -> None:
        """Update last sync time for a page"""
        if page_title in self.scheduled_tasks:
            now = datetime.now(timezone.utc)
            self.scheduled_tasks[page_title]["last_sync"] = now
            self.scheduled_tasks[page_title]["next_sync"] = now + timedelta(seconds=self.scheduled_tasks[page_title]["interval"])

class NotificationManager:
    """Manages notifications for sync events"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.subscribers = []
    
    def subscribe(self, callback) -> None:
        """Subscribe to sync notifications"""
        self.subscribers.append(callback)
    
    def notify_sync_start(self, page_title: str) -> None:
        """Notify subscribers about sync start"""
        for callback in self.subscribers:
            callback("sync_start", page_title)
    
    def notify_sync_complete(self, page_title: str, status: SyncStatus) -> None:
        """Notify subscribers about sync completion"""
        for callback in self.subscribers:
            callback("sync_complete", page_title, status)
    
    def notify_conflict(self, page_title: str) -> None:
        """Notify subscribers about conflicts"""
        for callback in self.subscribers:
            callback("conflict", page_title)

class MetricsCollector:
    """Collects performance metrics for wiki sync operations"""
    
    def __init__(self):
        self.metrics = {
            "total_syncs": 0,
            "successful_syncs": 0,
            "failed_syncs": 0,
            "conflict_resolutions": 0,
            "average_sync_time": 0.0,
            "last_sync_duration": 0.0
        }
        self.sync_times = []
    
    def record_sync_start(self) -> float:
        """Record sync start time"""
        return datetime.now(timezone.utc).timestamp()
    
    def record_sync_complete(self, start_time: float, success: bool, conflict: bool = False) -> None:
        """Record sync completion metrics"""
        end_time = datetime.now(timezone.utc).timestamp()
        duration = end_time - start_time
        
        self.metrics["total_syncs"] += 1
        self.sync_times.append(duration)
        
        if success:
            self.metrics["successful_syncs"] += 1
        else:
            self.metrics["failed_syncs"] += 1
        
        if conflict:
            self.metrics["conflict_resolutions"] += 1
        
        self.metrics["last_sync_duration"] = duration
        self.metrics["average_sync_time"] = sum(self.sync_times) / len(self.sync_times)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get collected metrics"""
        return self.metrics.copy()

# Phase 4: Production-Ready Features
# ==================================

class WikiSyncService:
    """Main service class for wiki synchronization"""
    
    def __init__(self, config_path: str = "config/wiki_sync.json"):
        self.config = WikiSyncConfig(config_path)
        self.api_client = WikiAPIClient(self.config)
        self.validator = ContentValidator()
        self.conflict_resolver = ConflictResolver(self.config.config.get("conflict_resolution", "manual"))
        self.scheduler = SyncScheduler(self.config.config.get("sync_interval", 3600))
        self.notification_manager = NotificationManager()
        self.metrics_collector = MetricsCollector()
        self.logger = self._setup_logging()
        self.sync_history = []
        
        # Initialize service
        self._initialize_service()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("WikiSyncService")
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(log_dir / "wiki_sync.log")
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_service(self) -> None:
        """Initialize the wiki sync service"""
        self.logger.info("Initializing Wiki Sync Service...")
        
        # Authenticate with wiki
        if not self.api_client.authenticate():
            self.logger.error("Failed to authenticate with wiki API")
            raise RuntimeError("Authentication failed")
        
        self.logger.info("Wiki Sync Service initialized successfully")
    
    def sync_page(self, page_title: str, local_content: str) -> SyncStatus:
        """Synchronize a single page"""
        self.logger.info(f"Starting sync for page: {page_title}")
        
        # Record sync start
        start_time = self.metrics_collector.record_sync_start()
        self.notification_manager.notify_sync_start(page_title)
        
        try:
            # Create local page object
            local_page = WikiPage(
                title=page_title,
                content=local_content,
                last_modified=datetime.now(timezone.utc),
                version=1,
                checksum=self.api_client._calculate_checksum(local_content),
                metadata={"source": "local"}
            )
            
            # Validate content
            is_valid, issues = self.validator.validate_content(local_content)
            if not is_valid:
                self.logger.warning(f"Content validation issues: {issues}")
            
            # Get remote page
            remote_page = self.api_client.get_page_content(page_title)
            
            # Determine sync action
            if remote_page is None:
                # New page - create it
                success = self.api_client.update_page(local_page)
                status = SyncStatus.COMPLETED if success else SyncStatus.FAILED
            
            elif remote_page.checksum == local_page.checksum:
                # No changes
                self.logger.info("No changes detected")
                status = SyncStatus.COMPLETED
            
            else:
                # Changes detected - resolve conflict
                resolved_page = self.conflict_resolver.resolve_conflict(local_page, remote_page)
                
                if resolved_page.checksum != remote_page.checksum:
                    success = self.api_client.update_page(resolved_page)
                    status = SyncStatus.COMPLETED if success else SyncStatus.FAILED
                else:
                    status = SyncStatus.COMPLETED
            
            # Record sync completion
            self.metrics_collector.record_sync_complete(
                start_time, 
                status == SyncStatus.COMPLETED,
                status == SyncStatus.CONFLICT
            )
            
            # Update sync history
            self.sync_history.append(SyncRecord(
                page_title=page_title,
                sync_time=datetime.now(timezone.utc),
                status=status,
                local_checksum=local_page.checksum,
                remote_checksum=remote_page.checksum if remote_page else "",
                changes_detected=remote_page is None or remote_page.checksum != local_page.checksum
            ))
            
            # Notify completion
            self.notification_manager.notify_sync_complete(page_title, status)
            
            self.logger.info(f"Sync completed for {page_title} with status: {status}")
            return status
            
        except Exception as e:
            self.logger.error(f"Sync failed for {page_title}: {str(e)}")
            self.metrics_collector.record_sync_complete(start_time, False)
            self.notification_manager.notify_sync_complete(page_title, SyncStatus.FAILED)
            
            # Record failed sync
            self.sync_history.append(SyncRecord(
                page_title=page_title,
                sync_time=datetime.now(timezone.utc),
                status=SyncStatus.FAILED,
                local_checksum="",
                remote_checksum="",
                changes_detected=False,
                error_message=str(e)
            ))
            
            return SyncStatus.FAILED
    
    def sync_directory(self, directory_path: str, pattern: str = "*.md") -> Dict[str, SyncStatus]:
        """Synchronize all files in a directory"""
        self.logger.info(f"Starting directory sync: {directory_path}")
        
        results = {}
        directory = Path(directory_path)
        
        if not directory.exists():
            self.logger.error(f"Directory does not exist: {directory_path}")
            return results
        
        for file_path in directory.rglob(pattern):
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    page_title = file_path.stem.replace('_', ' ').title()
                    status = self.sync_page(page_title, content)
                    results[str(file_path)] = status
                    
                except Exception as e:
                    self.logger.error(f"Failed to sync {file_path}: {str(e)}")
                    results[str(file_path)] = SyncStatus.FAILED
        
        return results
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync status and metrics"""
        return {
            "service_status": "running",
            "last_sync_time": self.sync_history[-1].sync_time if self.sync_history else None,
            "total_syncs": len(self.sync_history),
            "metrics": self.metrics_collector.get_metrics(),
            "recent_syncs": [asdict(record) for record in self.sync_history[-10:]]
        }
    
    def schedule_automatic_sync(self, page_titles: List[str], interval: Optional[int] = None) -> bool:
        """Schedule automatic synchronization for pages"""
        try:
            for page_title in page_titles:
                self.scheduler.schedule_sync(page_title, interval)
            
            self.logger.info(f"Scheduled automatic sync for {len(page_titles)} pages")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to schedule automatic sync: {str(e)}")
            return False
    
    def cleanup_old_sync_records(self, days_to_keep: int = 30) -> int:
        """Clean up old sync records"""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)
        original_count = len(self.sync_history)
        
        self.sync_history = [
            record for record in self.sync_history
            if record.sync_time > cutoff_date
        ]
        
        removed_count = original_count - len(self.sync_history)
        self.logger.info(f"Cleaned up {removed_count} old sync records")
        
        return removed_count
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on the service"""
        health_status = {
            "service": "healthy",
            "api_connection": False,
            "authentication": False,
            "last_error": None
        }
        
        try:
            # Test API connection
            response = requests.get(
                self.config.config["wiki_api_url"],
                timeout=5,
                params={"action": "query", "format": "json"}
            )
            health_status["api_connection"] = response.status_code == 200
            
            # Test authentication
            health_status["authentication"] = self.api_client.authenticate()
            
        except Exception as e:
            health_status["service"] = "unhealthy"
            health_status["last_error"] = str(e)
        
        return health_status

# Usage Example
if __name__ == "__main__":
    # Initialize service
    service = WikiSyncService()
    
    # Example usage
    try:
        # Sync a single page
        status = service.sync_page("Project Documentation", "# Project Overview\n\nThis is the main documentation.")
        print(f"Sync status: {status}")
        
        # Get service status
        status_info = service.get_sync_status()
        print(json.dumps(status_info, indent=2, default=str))
        
    except Exception as e:
        print(f"Error: {str(e)}")
