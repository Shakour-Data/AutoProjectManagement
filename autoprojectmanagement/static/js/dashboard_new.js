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
            toggleBtn.innerHTML = widgetConfig.enabled ? '👁️' : '👁️‍🗨️';
            toggleBtn.title = widgetConfig.enabled ? 'Disable widget' : 'Enable widget';
            toggleBtn.onclick = () => this.toggleWidget(widgetId);
            
            const configBtn = document.createElement('button');
            configBtn.className = 'widget-toggle';
            configBtn.innerHTML = '⚙️';
            configBtn.title = 'Configure widget';
            configBtn.onclick = () => this.showConfigModal(widgetId);
            
            controls.appendChild(toggleBtn);
            controls.appendChild(configBtn);
            
            header.appendChild(title);
            header.appendChild(controls);
            
            // Insert header at the beginning of the widget
            widget.insertBefore(header, widget.firstChild);
        });
    }

    removeWidgetControls() {
        const headers = document.querySelectorAll('.widget-header');
        headers.forEach(header => header.remove());
    }

    getWidgetName(widgetId) {
        const names = {
            'health': 'Project Health',
            'progress': 'Task Progress',
            'risks': 'Risk Assessment',
            'team': 'Team Performance',
            'quality': 'Quality Metrics',
            'alerts': 'Active Alerts'
        };
        return names[widgetId] || widgetId;
    }

    toggleWidget(widgetId) {
        const widget = this.currentLayout.widgets.find(w => w.widget_id === widgetId);
        if (widget) {
            widget.enabled = !widget.enabled;
            
            // Update UI
            const widgetElement = document.querySelector(`[data-widget-id="${widgetId}"]`);
            if (widgetElement) {
                widgetElement.style.opacity = widget.enabled ? '1' : '0.5';
                
                const toggleBtn = widgetElement.querySelector('.widget-toggle');
                if (toggleBtn) {
                    toggleBtn.innerHTML = widget.enabled ? '👁️' : '👁️‍🗨️';
                    toggleBtn.title = widget.enabled ? 'Disable widget' : 'Enable widget';
                }
            }
        }
    }

    showConfigModal(widgetId) {
        const widget = this.currentLayout.widgets.find(w => w.widget_id === widgetId);
        if (widget) {
            this.currentEditingWidget = widgetId;
            
            // Populate form
            document.getElementById('widgetEnabled').checked = widget.enabled;
            document.getElementById('widgetRefreshRate').value = this.currentLayout.refresh_rate;
            document.getElementById('widgetTheme').value = this.currentLayout.theme;
            
            // Show modal
            document.getElementById('widgetConfigModal').style.display = 'flex';
        }
    }

    hideConfigModal() {
        document.getElementById('widgetConfigModal').style.display = 'none';
        this.currentEditingWidget = null;
    }

    saveWidgetConfig() {
        if (this.currentEditingWidget) {
            const widget = this.currentLayout.widgets.find(w => w.widget_id === this.currentEditingWidget);
            if (widget) {
                widget.enabled = document.getElementById('widgetEnabled').checked;
                this.currentLayout.refresh_rate = parseInt(document.getElementById('widgetRefreshRate').value);
                this.currentLayout.theme = document.getElementById('widgetTheme').value;
                
                // Update refresh rate
                this.refreshRate = this.currentLayout.refresh_rate;
                this.updateRefreshRate();
                
                // Update theme (would need theme switching implementation)
                console.log('Theme changed to:', this.currentLayout.theme);
            }
            
            this.hideConfigModal();
        }
    }

    async loadLayout(layoutType) {
        try {
            this.showLoading(true);
            
            const response = await fetch(`/api/v1/dashboard/layout?layout_type=${layoutType}`);
            if (!response.ok) throw new Error('Failed to load layout');
            
            this.currentLayout = await response.json();
            this.applyLayout();
            
            // Update selector
            document.getElementById('layoutSelector').value = layoutType;
            
        } catch (error) {
            console.error('Error loading layout:', error);
            this.showError('Failed to load layout');
        } finally {
            this.showLoading(false);
        }
    }

    applyLayout() {
        const widgetsGrid = document.querySelector('.widgets-grid');
        widgetsGrid.innerHTML = '';
        
        // Sort widgets by position
        const sortedWidgets = [...this.currentLayout.widgets].sort((a, b) => a.position - b.position);
        
        sortedWidgets.forEach(widgetConfig => {
            if (widgetConfig.enabled) {
                const widgetElement = this.createWidgetElement(widgetConfig.widget_id);
                if (widgetElement) {
                    widgetsGrid.appendChild(widgetElement);
                }
            }
        });
        
        // Update theme if needed
        if (this.currentLayout.theme !== 'light') {
            console.log('Applying theme:', this.currentLayout.theme);
            // Theme switching would be implemented here
        }
    }

    createWidgetElement(widgetId) {
        const templates = {
            'health': () => `<div class="widget health-widget" data-widget-id="health">
                <h3>Project Health</h3>
                <div class="widget-content">
                    <canvas id="healthChart"></canvas>
                </div>
            </div>`,
            'progress': () => `<div class="widget progress-widget" data-widget-id="progress">
                <h3>Task Progress</h3>
                <div class="widget-content">
                    <canvas id="progressChart"></canvas>
                </div>
            </div>`,
            'risks': () => `<div class="widget risk-widget" data-widget-id="risks">
                <h3>Risk Assessment</h3>
                <div class="widget-content">
                    <div class="risk-matrix" id="riskMatrix"></div>
                </div>
            </div>`,
            'team': () => `<div class="widget team-widget" data-widget-id="team">
                <h3>Team Performance</h3>
                <div class="widget-content">
                    <canvas id="teamChart"></canvas>
                </div>
            </div>`,
            'quality': () => `<div class="widget quality-widget" data-widget-id="quality">
                <h3>Quality Metrics</h3>
                <div class="widget-content">
                    <canvas id="qualityChart"></canvas>
                </div>
            </div>`,
            'alerts': () => `<div class="widget alerts-widget" data-widget-id="alerts">
                <h3>Active Alerts</h3>
                <div class="widget-content">
                    <div class="alerts-list" id="alertsList"></div>
                </div>
            </div>`
        };
        
        const template = templates[widgetId];
        if (template) {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = template();
            return tempDiv.firstChild;
        }
        
        return null;
    }

    async saveLayout() {
        try {
            this.showLoading(true);
            
