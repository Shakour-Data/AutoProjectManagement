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
