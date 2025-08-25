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
