// Dashboard JavaScript for AutoProjectManagement
document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    const API_BASE_URL = 'http://localhost:8000/api/v1';
    const DASHBOARD_ENDPOINTS = {
        overview: '/dashboard/overview',
        metrics: '/dashboard/metrics',
        alerts: '/dashboard/alerts',
        health: '/dashboard/health'
    };

    // State management
    let dashboardData = {
        overview: null,
        metrics: null,
        alerts: null,
        health: null
    };

    // Initialize dashboard
    initializeDashboard();

    // Main initialization function
    function initializeDashboard() {
        console.log('Initializing dashboard...');
        
        // Show loading states
        showLoadingStates();
        
        // Load all dashboard data
        loadDashboardData();
        
        // Set up periodic refresh (every 30 seconds)
        setInterval(loadDashboardData, 30000);
        
        // Set up event listeners
        setupEventListeners();
    }

    // Show loading states for all sections
    function showLoadingStates() {
        const sections = ['overview', 'metrics', 'alerts'];
        sections.forEach(section => {
            const element = document.getElementById(`${section}-content`);
            if (element) {
                element.innerHTML = '<div class="loading">Loading ' + section + ' data...</div>';
            }
        });
    }

    // Load all dashboard data
    async function loadDashboardData() {
        try {
            console.log('Loading dashboard data...');
            
            // Load data in parallel
            const [overviewData, metricsData, alertsData, healthData] = await Promise.allSettled([
                fetchData('overview'),
                fetchData('metrics'),
                fetchData('alerts'),
                fetchData('health')
            ]);

            // Update dashboard data state
            dashboardData.overview = overviewData.status === 'fulfilled' ? overviewData.value : null;
            dashboardData.metrics = metricsData.status === 'fulfilled' ? metricsData.value : null;
            dashboardData.alerts = alertsData.status === 'fulfilled' ? alertsData.value : null;
            dashboardData.health = healthData.status === 'fulfilled' ? healthData.value : null;

            // Update UI
            updateDashboardUI();

        } catch (error) {
            console.error('Error loading dashboard data:', error);
            showErrorStates();
        }
    }

    // Fetch data from API endpoint
    async function fetchData(endpoint) {
        try {
            const url = `${API_BASE_URL}${DASHBOARD_ENDPOINTS[endpoint]}?project_id=default`;
            const response = await fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`Error fetching ${endpoint} data:`, error);
            throw error;
        }
    }

    // Update dashboard UI with loaded data
    function updateDashboardUI() {
        updateOverview();
        updateMetrics();
        updateAlerts();
        updateHealthStatus();
    }

    // Update overview section
    function updateOverview() {
        const overviewContent = document.getElementById('overview-content');
        if (!overviewContent) return;

        if (dashboardData.overview) {
            overviewContent.innerHTML = `
                <div class="success">
                    <h3>Project Overview</h3>
                    <p><strong>Project ID:</strong> ${dashboardData.overview.project_id || 'N/A'}</p>
                    <p><strong>Status:</strong> <span class="status-active">Active</span></p>
                    <p><strong>Last Updated:</strong> ${new Date().toLocaleString()}</p>
                </div>
            `;
        } else {
            overviewContent.innerHTML = `
                <div class="error">
                    <h3>Overview Unavailable</h3>
                    <p>Unable to load project overview data.</p>
                    <button onclick="loadDashboardData()">Retry</button>
                </div>
            `;
        }
    }

    // Update metrics section
    function updateMetrics() {
        const metricsContent = document.getElementById('metrics-content');
        if (!metricsContent) return;

        if (dashboardData.metrics) {
            metricsContent.innerHTML = `
                <div>
                    <h3>Project Metrics</h3>
                    <p><strong>Tasks Completed:</strong> ${dashboardData.metrics.tasks_completed || 0}</p>
                    <p><strong>Tasks Pending:</strong> ${dashboardData.metrics.tasks_pending || 0}</p>
                    <p><strong>Progress:</strong> ${dashboardData.metrics.progress_percentage || 0}%</p>
                </div>
            `;
        } else {
            metricsContent.innerHTML = `
                <div class="error">
                    <h3>Metrics Unavailable</h3>
                    <p>Unable to load project metrics.</p>
                    <button onclick="loadDashboardData()">Retry</button>
                </div>
            `;
        }
    }

    // Update alerts section
    function updateAlerts() {
        const alertsContent = document.getElementById('alerts-content');
        if (!alertsContent) return;

        if (dashboardData.alerts && Array.isArray(dashboardData.alerts) && dashboardData.alerts.length > 0) {
            const alertsHTML = dashboardData.alerts.map(alert => `
                <div class="alert-item">
                    <strong>${alert.severity || 'INFO'}:</strong> ${alert.message || 'No message'}
                    <small>${new Date(alert.timestamp).toLocaleString()}</small>
                </div>
            `).join('');

            alertsContent.innerHTML = `
                <div>
                    <h3>Active Alerts (${dashboardData.alerts.length})</h3>
                    ${alertsHTML}
                </div>
            `;
        } else {
            alertsContent.innerHTML = `
                <div class="success">
                    <h3>No Active Alerts</h3>
                    <p>All systems are operating normally.</p>
                </div>
            `;
        }
    }

    // Update health status (hidden indicator)
    function updateHealthStatus() {
        // This could be used for visual indicators or logging
        console.log('System health:', dashboardData.health);
    }

    // Show error states for all sections
    function showErrorStates() {
        const sections = ['overview', 'metrics', 'alerts'];
        sections.forEach(section => {
            const element = document.getElementById(`${section}-content`);
            if (element) {
                element.innerHTML = `
                    <div class="error">
                        <h3>Connection Error</h3>
                        <p>Unable to connect to the server.</p>
                        <button onclick="loadDashboardData()">Retry Connection</button>
                    </div>
                `;
            }
        });
    }

    // Set up event listeners
    function setupEventListeners() {
        // Refresh button (if added to HTML)
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', loadDashboardData);
        }

        // Responsive menu toggle (if added to HTML)
        const menuToggle = document.getElementById('menu-toggle');
        if (menuToggle) {
            menuToggle.addEventListener('click', toggleMobileMenu);
        }

        // Window resize for responsive adjustments
        window.addEventListener('resize', handleResize);
    }

    // Handle window resize for responsive design
    function handleResize() {
        // Additional responsive adjustments can be added here
        console.log('Window resized:', window.innerWidth);
    }

    // Toggle mobile menu (if implemented)
    function toggleMobileMenu() {
        const nav = document.querySelector('nav');
        if (nav) {
            nav.classList.toggle('mobile-visible');
        }
    }

    // Utility function to format numbers
    function formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }

    // Utility function to format dates
    function formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    }

    // Make functions available globally for HTML onclick attributes
    window.loadDashboardData = loadDashboardData;
    window.toggleMobileMenu = toggleMobileMenu;
});

// Service Worker registration for PWA capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Offline detection
window.addEventListener('online', function() {
    console.log('Connection restored');
    document.body.classList.remove('offline');
    // Optionally trigger data refresh
    if (typeof loadDashboardData === 'function') {
        loadDashboardData();
    }
});

window.addEventListener('offline', function() {
    console.log('Connection lost');
    document.body.classList.add('offline');
});
