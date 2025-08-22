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
