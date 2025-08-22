// AutoProjectManagement Dashboard JavaScript
class Dashboard {
    constructor() {
        this.projectId = null;
        this.refreshRate = 3000;
        this.socket = null;
        this.charts = {};
        this.isConnected = false;
        
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
            };

            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };

            this.socket.onclose = () => {
                this.isConnected = false;
                this.updateConnectionStatus(false);
                console.log('WebSocket disconnected');
                
                // Attempt reconnection after delay
                setTimeout(() => this.connectWebSocket(), 5000);
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.isConnected = false;
                this.updateConnectionStatus(false);
            };

        } catch (error) {
            console.error('WebSocket connection failed:', error);
            this.isConnected = false;
            this.updateConnectionStatus(false);
        }
    }

    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'initial':
                console.log('WebSocket initialized:', data.message);
                break;
                
            case 'update':
                this.handleRealTimeUpdate(data);
                break;
                
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    handleRealTimeUpdate(data) {
        // Highlight updated elements
        this.highlightUpdates();
        
        // Update metrics if available
        if (data.metrics) {
            this.updateCharts({ metrics: data.metrics, trends: data.trends || {} });
        }
        
        // Update alerts if available
        if (data.alerts) {
            this.updateAlerts(data.alerts);
        }
        
        this.updateLastUpdated();
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
