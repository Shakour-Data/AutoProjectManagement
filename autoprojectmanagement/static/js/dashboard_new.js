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
        this.isEditMode = false;
        this.sortable = null;
        this.currentLayout = null;
        this.currentEditingWidget = null;
        
        this.initialize();
    }

    initialize() {
        this.setupEventListeners();
        this.setupLayoutControls();
        this.loadProjectData();
        this.connectWebSocket();
        this.initializeCharts();
        this.populateLayoutSelector();
        this.loadLayout('standard');
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

    // Layout Management Methods
    setupLayoutControls() {
        // Edit layout button
        document.getElementById('editLayoutBtn').addEventListener('click', () => {
            this.enterEditMode();
        });

        // Save layout button
        document.getElementById('saveLayoutBtn').addEventListener('click', () => {
            this.saveLayout();
        });

        // Cancel edit button
        document.getElementById('cancelLayoutBtn').addEventListener('click', () => {
            this.exitEditMode();
        });

        // Layout selector
        document.getElementById('layoutSelector').addEventListener('change', (e) => {
            this.loadLayout(e.target.value);
        });

        // Modal controls
        document.getElementById('closeConfigModal').addEventListener('click', () => {
            this.hideConfigModal();
        });

        document.getElementById('cancelWidgetConfig').addEventListener('click', () => {
            this.hideConfigModal();
        });

        document.getElementById('saveWidgetConfig').addEventListener('click', () => {
            this.saveWidgetConfig();
        });
    }

    enterEditMode() {
        this.isEditMode = true;
        document.body.classList.add('widget-edit-mode');
        
        // Show save/cancel buttons, hide edit button
        document.getElementById('editLayoutBtn').style.display = 'none';
        document.getElementById('saveLayoutBtn').style.display = 'inline-block';
        document.getElementById('cancelLayoutBtn').style.display = 'inline-block';
        
        // Initialize drag and drop
        this.initializeDragAndDrop();
        
        // Add widget controls
        this.addWidgetControls();
    }

    exitEditMode() {
        this.isEditMode = false;
        document.body.classList.remove('widget-edit-mode');
        
        // Show edit button, hide save/cancel buttons
        document.getElementById('editLayoutBtn').style.display = 'inline-block';
        document.getElementById('saveLayoutBtn').style.display = 'none';
        document.getElementById('cancelLayoutBtn').style.display = 'none';
        
        // Remove drag and drop
        this.destroyDragAndDrop();
        
        // Remove widget controls
        this.removeWidgetControls();
        
        // Reload current layout to reset any changes
        this.loadLayout(document.getElementById('layoutSelector').value);
    }

    initializeDragAndDrop() {
        const widgetsGrid = document.querySelector('.widgets-grid');
        
        this.sortable = Sortable.create(widgetsGrid, {
            animation: 150,
            ghostClass: 'widget-dragging',
            chosenClass: 'widget-dragging',
            dragClass: 'widget-dragging',
            onEnd: (evt) => {
                this.updateWidgetPositions();
            }
        });
    }

    destroyDragAndDrop() {
        if (this.sortable) {
            this.sortable.destroy();
            this.sortable = null;
        }
    }

    updateWidgetPositions() {
        const widgets = document.querySelectorAll('.widget');
        this.currentLayout.widgets = Array.from(widgets).map((widget, index) => {
            const widgetId = widget.dataset.widgetId;
            const currentWidget = this.currentLayout.widgets.find(w => w.widget_id === widgetId);
            
            return {
                widget_id: widgetId,
                position: index,
                enabled: currentWidget ? currentWidget.enabled : true,
                settings: currentWidget ? currentWidget.settings : {}
            };
        });
    }

    addWidgetControls() {
        const widgets = document.querySelectorAll('.widget');
        
        widgets.forEach(widget => {
            const widgetId = widget.dataset.widgetId;
            const widgetConfig = this.currentLayout.widgets.find(w => w.widget_id === widgetId);
            
            // Create widget header with controls
            const header = document.createElement('div');
            header.className = 'widget-header';
            
            const title = document.createElement('h4');
            title.className = 'widget-title';
            title.textContent = this.getWidgetName(widgetId);
            
            const controls = document.createElement('div');
            controls.className = 'widget-controls';
            
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'widget-toggle';
