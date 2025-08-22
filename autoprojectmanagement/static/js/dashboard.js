// AutoProjectManagement Dashboard JavaScript
class Dashboard {
    constructor() {
        this.projectId = null;
        this.refreshRate = 3000;
        this.socket = null;
        this.charts = {};
        this.isConnected = false;
        this.lastEventId = localStorage.getItem('lastEventId') || null;
        this.heartbeatInterval = null;
        this.reconnectAttempts = 0;
        
        this.initialize();
    }

    initialize() {
        this.setupEventListeners();
        this.loadProjectData();
        this.connectWebSocket();
        this.initializeCharts();
    }

    setupEventListeners() {
        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadProjectData();
        });

        // Refresh rate selector
        document.getElementById('refreshRate').addEventListener('change', (e) => {
            this.refreshRate = parseInt(e.target.value);
            this.updateRefreshRate();
        });

        // Handle window focus for reconnection
        window.addEventListener('focus', () => {
            if (!this.isConnected) {
                this.connectWebSocket();
            }
        });
    }

    async loadProjectData() {
        try {
            this.showLoading(true);
            
            // In a real implementation, we would get the project ID from URL or configuration
            const projectId = this.projectId || 'default';
            
            // Load overview data
            const overviewResponse = await fetch(`/api/v1/dashboard/overview?project_id=${projectId}`);
            if (!overviewResponse.ok) throw new Error('Failed to load overview');
            const overviewData = await overviewResponse.json();
            
            // Load metrics data
            const metricsResponse = await fetch(`/api/v1/dashboard/metrics?project_id=${projectId}&timeframe=24h`);
            const metricsData = metricsResponse.ok ? await metricsResponse.json() : null;
            
            // Load alerts
            const alertsResponse = await fetch(`/api/v1/dashboard/alerts?project_id=${projectId}`);
            const alertsData = alertsResponse.ok ? await alertsResponse.json() : [];
            
            this.updateDashboard(overviewData, metricsData, alertsData);
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data');
        } finally {
            this.showLoading(false);
        }
    }

    updateDashboard(overview, metrics, alerts) {
        // Update overview section
        this.updateOverview(overview);
        
        // Update charts with metrics
        if (metrics) {
            this.updateCharts(metrics);
        }
        
        // Update alerts
        this.updateAlerts(alerts);
        
        // Update last updated timestamp
        this.updateLastUpdated();
    }

    updateOverview(data) {
        document.getElementById('projectId').textContent = `Project: ${data.project_id}`;
        document.getElementById('totalTasks').textContent = data.total_tasks;
        document.getElementById('completedTasks').textContent = data.completed_tasks;
        document.getElementById('progressPercentage').textContent = `${data.progress_percentage}%`;
        
        const riskElement = document.getElementById('riskLevel');
        riskElement.textContent = data.risk_level;
        riskElement.className = `stat-value risk-level ${data.risk_level}`;
        
        const healthScore = document.getElementById('healthScore').querySelector('.score-value');
        healthScore.textContent = `${data.health_score}%`;
        healthScore.style.color = this.getHealthColor(data.health_score);
    }

    getHealthColor(score) {
        if (score >= 80) return '#10b981'; // Green
        if (score >= 60) return '#f59e0b'; // Orange
        return '#ef4444'; // Red
    }

    initializeCharts() {
        // Health Chart
        this.charts.health = new Chart(document.getElementById('healthChart'), {
            type: 'doughnut',
            data: {
                labels: ['Health Score'],
                datasets: [{
                    data: [0],
                    backgroundColor: ['#2563eb'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });

        // Progress Chart
        this.charts.progress = new Chart(document.getElementById('progressChart'), {
            type: 'bar',
            data: {
                labels: ['Completed', 'Remaining'],
                datasets: [{
                    data: [0, 0],
                    backgroundColor: ['#10b981', '#e2e8f0'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { display: false },
                    x: { display: true }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });

        // Team Performance Chart
        this.charts.team = new Chart(document.getElementById('teamChart'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Velocity',
                    data: [],
                    borderColor: '#2563eb',
                    tension: 0.1,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

        // Quality Chart
        this.charts.quality = new Chart(document.getElementById('qualityChart'), {
            type: 'radar',
            data: {
                labels: ['Test Coverage', 'Code Quality', 'Bug Density'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: 'rgba(37, 99, 235, 0.2)',
                    borderColor: '#2563eb',
                    pointBackgroundColor: '#2563eb'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    updateCharts(metrics) {
        // Update health chart
        if (this.charts.health) {
            this.charts.health.data.datasets[0].data = [metrics.metrics.health_score || 0];
            this.charts.health.update();
        }

        // Update progress chart
        if (this.charts.progress && metrics.metrics) {
            const completed = metrics.metrics.completed_tasks || 0;
            const total = metrics.metrics.total_tasks || 1;
            this.charts.progress.data.datasets[0].data = [completed, total - completed];
            this.charts.progress.update();
        }

        // Update team performance chart
        if (this.charts.team && metrics.trends) {
            const velocityData = metrics.trends.velocity || [];
            this.charts.team.data.labels = velocityData.map((_, i) => `Day ${i + 1}`);
            this.charts.team.data.datasets[0].data = velocityData;
            this.charts.team.update();
        }

        // Update quality chart
        if (this.charts.quality && metrics.metrics.quality_metrics) {
            const quality = metrics.metrics.quality_metrics;
            this.charts.quality.data.datasets[0].data = [
                quality.test_coverage || 0,
                quality.code_quality || 0,
                100 - (quality.bug_density || 0) * 10 // Scale bug density
            ];
            this.charts.quality.update();
        }
    }

    updateAlerts(alerts) {
        const alertsList = document.getElementById('alertsList');
        alertsList.innerHTML = '';

        if (alerts.length === 0) {
            alertsList.innerHTML = '<div class="no-alerts">No active alerts</div>';
            return;
        }

        alerts.forEach(alert => {
            const alertElement = document.createElement('div');
            alertElement.className = `alert-item alert-${alert.severity}`;
            
            alertElement.innerHTML = `
                <div class="alert-header">
                    <span class="alert-type">${alert.type}</span>
                    <span class="alert-severity">${alert.severity}</span>
                </div>
                <div class="alert-message">${alert.message}</div>
                <div class="alert-time">${new Date(alert.timestamp).toLocaleString()}</div>
            `;
            
            alertsList.appendChild(alertElement);
        });
    }

    updateLastUpdated() {
        document.getElementById('lastUpdated').textContent = new Date().toLocaleString();
    }

    connectWebSocket() {
        try {
            // Close existing connection if any
            if (this.socket) {
                this.socket.close();
            }

            // Connect to WebSocket
            this.socket = new WebSocket(`ws://${window.location.host}/api/v1/dashboard/ws`);
            
            this.socket.onopen = () => {
                this.isConnected = true;
                this.updateConnectionStatus(true);
                console.log('WebSocket connected');
                
                // Send reconnection request with last event ID if available
                const subscriptionData = {
                    type: 'subscribe',
                    event_types: [
                        'file_change',
                        'auto_commit',
                        'progress_update',
                    'risk_alert',
                        'dashboard_update',
                        'auto_commit_start',
                        'auto_commit_result',
                        'auto_commit_error'
                    ],
                    project_id: this.projectId || 'default',
                    last_event_id: this.lastEventId // Send last received event ID for reconnection
                };
                
                this.socket.send(JSON.stringify(subscriptionData));
                
                // Start heartbeat
                this.startHeartbeat();
            };

            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
                
                // Update last event ID for reconnection support
                if (data.event_id && !data.is_replay) {
                    this.lastEventId = data.event_id;
                    localStorage.setItem('lastEventId', this.lastEventId);
                }
            };

            this.socket.onclose = () => {
                this.isConnected = false;
                this.updateConnectionStatus(false);
                console.log('WebSocket disconnected');
                
                // Stop heartbeat
                this.stopHeartbeat();
                
                // Attempt reconnection with exponential backoff
                this.attemptReconnection();
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.isConnected = false;
                this.updateConnectionStatus(false);
                
                // Stop heartbeat on error
                this.stopHeartbeat();
            };

        } catch (error) {
            console.error('WebSocket connection failed:', error);
            this.isConnected = false;
            this.updateConnectionStatus(false);
        }
    }

    subscribeToEvents(eventTypes) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                type: 'subscribe',
                event_types: eventTypes,
                project_id: this.projectId || 'default',
                last_event_id: this.lastEventId
            }));
        }
    }

    startHeartbeat() {
        // Clear existing heartbeat if any
        this.stopHeartbeat();
        
        // Send ping every 25 seconds (slightly less than server timeout)
        this.heartbeatInterval = setInterval(() => {
            if (this.socket && this.socket.readyState === WebSocket.OPEN) {
                this.socket.send(JSON.stringify({
                    type: 'ping',
                    timestamp: Date.now()
                }));
            }
        }, 25000);
    }

    stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }

    attemptReconnection() {
        // Exponential backoff for reconnection
        const maxAttempts = 5;
        const baseDelay = 1000; // 1 second
        const maxDelay = 30000; // 30 seconds
        
        if (this.reconnectAttempts >= maxAttempts) {
            console.log('Max reconnection attempts reached, giving up');
            this.reconnectAttempts = 0;
            return;
        }
        
        const delay = Math.min(baseDelay * Math.pow(2, this.reconnectAttempts), maxDelay);
        this.reconnectAttempts++;
        
        console.log(`Attempting reconnection in ${delay}ms (attempt ${this.reconnectAttempts}/${maxAttempts})`);
        
        setTimeout(() => {
            this.connectWebSocket();
        }, delay);
    }

    handleWebSocketMessage(data) {
        console.log('WebSocket message received:', data);
        
        switch (data.type) {
            case 'connection_established':
                console.log('WebSocket connection established:', data.message);
                break;
                
            case 'subscription_confirmed':
                console.log('Subscription confirmed:', data.event_types);
                break;
                
            case 'event':
                this.handleRealTimeEvent(data.event_type, data.data);
                break;
                
            case 'heartbeat':
                // Keep connection alive, no action needed
                break;
                
            case 'pong':
                // Response to ping, no action needed
                break;
                
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    handleRealTimeEvent(eventType, eventData) {
        console.log(`Handling event: ${eventType}`, eventData);
        
        switch (eventType) {
            case 'file_change':
                this.handleFileChangeEvent(eventData);
                break;
                
            case 'auto_commit':
                this.handleAutoCommitEvent(eventData);
                break;
                
            case 'auto_commit_start':
                this.handleAutoCommitStartEvent(eventData);
                break;
                
            case 'auto_commit_result':
                this.handleAutoCommitResultEvent(eventData);
                break;
                
            case 'auto_commit_error':
                this.handleAutoCommitErrorEvent(eventData);
                break;
                
            case 'progress_update':
                this.handleProgressUpdateEvent(eventData);
                break;
                
            case 'risk_alert':
                this.handleRiskAlertEvent(eventData);
                break;
                
            case 'dashboard_update':
                this.handleDashboardUpdateEvent(eventData);
                break;
                
            case 'health_check':
                // Heartbeat received, no action needed
                console.log('Heartbeat received');
                break;
                
            default:
                console.log('Unknown event type:', eventType);
        }
        
        // Always update last updated timestamp
        this.updateLastUpdated();
    }

    handleFileChangeEvent(data) {
        // Update file change counter
        const fileChangeElement = document.getElementById('fileChanges');
        if (fileChangeElement) {
            const currentCount = parseInt(fileChangeElement.textContent) || 0;
            fileChangeElement.textContent = currentCount + 1;
            this.highlightElement(fileChangeElement);
        }
        
        // Show notification
        this.showNotification(`File ${data.change_type}: ${data.file_path}`, 'info');
    }

    handleAutoCommitEvent(data) {
        if (data.event === 'start') {
            this.showNotification('Auto-commit started...', 'info');
        } else if (data.event === 'result') {
            const status = data.success ? 'success' : 'warning';
            const message = data.success ? 
                `Auto-commit completed successfully (${data.changes_count} changes)` :
                `Auto-commit completed with warnings (${data.changes_count} changes)`;
            
            this.showNotification(message, status);
        } else if (data.event === 'error') {
            this.showNotification(`Auto-commit error: ${data.error}`, 'error');
        }
    }

    handleProgressUpdateEvent(data) {
        // Update progress metrics
        if (data.progress_percentage !== undefined) {
            const progressElement = document.getElementById('progressPercentage');
            if (progressElement) {
                progressElement.textContent = `${data.progress_percentage}%`;
                this.highlightElement(progressElement);
            }
        }
        
        if (data.completed_tasks !== undefined && data.total_tasks !== undefined) {
            const completedElement = document.getElementById('completedTasks');
            const totalElement = document.getElementById('totalTasks');
            
            if (completedElement) completedElement.textContent = data.completed_tasks;
            if (totalElement) totalElement.textContent = data.total_tasks;
        }
        
        // Update charts if data is available
        if (data.metrics) {
            this.updateCharts({ metrics: data.metrics, trends: data.trends || {} });
        }
    }

    handleRiskAlertEvent(data) {
        // Add alert to alerts list
        this.showNotification(`Risk Alert: ${data.message}`, data.severity);
        
        // You could also update a risk indicator on the dashboard
        const riskElement = document.getElementById('riskLevel');
        if (riskElement && data.severity) {
            riskElement.textContent = data.severity;
            riskElement.className = `stat-value risk-level ${data.severity}`;
        }
    }

    handleDashboardUpdateEvent(data) {
        // Comprehensive dashboard update
        this.highlightUpdates();
        
        if (data.metrics) {
            this.updateCharts({ metrics: data.metrics, trends: data.trends || {} });
        }
        
        if (data.alerts) {
            this.updateAlerts(data.alerts);
        }
        
        if (data.overview) {
            this.updateOverview(data.overview);
        }
    }

    highlightElement(element) {
        element.classList.add('highlight');
        setTimeout(() => element.classList.remove('highlight'), 1000);
    }

    highlightUpdates() {
        const elements = document.querySelectorAll('.stat-value, .score-value');
        elements.forEach(el => {
            el.classList.add('highlight');
            setTimeout(() => el.classList.remove('highlight'), 1000);
        });
    }

    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connectionStatus');
        statusElement.textContent = connected ? 'Connected' : 'Disconnected';
        statusElement.className = connected ? 'connected' : 'disconnected';
    }

    updateRefreshRate() {
        // In a real implementation, this would update the WebSocket refresh rate
        console.log('Refresh rate updated to:', this.refreshRate);
    }

    showLoading(show) {
        document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
    }

    showError(message) {
        // Simple error display - could be enhanced with a proper notification system
        console.error('Dashboard error:', message);
        alert(`Error: ${message}`);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Dashboard;
}
