
const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

let statusBarItem;

function activate(context) {
    console.log('AutoProjectManagement Status Bar extension is now active!');
    
    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    
    // Set initial status
    updateStatusBar('Initializing...');
    statusBarItem.show();
    
    // Register commands
    let startCommand = vscode.commands.registerCommand('autoProjectManagement.start', function () {
        updateStatusBar('Running...');
        vscode.window.showInformationMessage('Auto Project Management started');
    });
    
    let stopCommand = vscode.commands.registerCommand('autoProjectManagement.stop', function () {
        updateStatusBar('Stopped');
        vscode.window.showInformationMessage('Auto Project Management stopped');
    });
    
    let refreshCommand = vscode.commands.registerCommand('autoProjectManagement.refreshStatus', function () {
        refreshProjectStatus();
    });
    
    let showDetailsCommand = vscode.commands.registerCommand('autoProjectManagement.showDetails', function () {
        showProjectDetails();
    });
    
    // Auto refresh every 30 seconds
    setInterval(refreshProjectStatus, 30000);
    
    // Initial refresh
    refreshProjectStatus();
    
    context.subscriptions.push(statusBarItem);
    context.subscriptions.push(startCommand);
    context.subscriptions.push(stopCommand);
    context.subscriptions.push(refreshCommand);
    context.subscriptions.push(showDetailsCommand);
}

function deactivate() {
    if (statusBarItem) {
        statusBarItem.dispose();
    }
}

function updateStatusBar(text, tooltip = null) {
    statusBarItem.text = `$(sync~spin) AutoPM: ${text}`;
    if (tooltip) {
        statusBarItem.tooltip = tooltip;
    }
}

function refreshProjectStatus() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceFolder) return;
    
    const statusFile = path.join(workspaceFolder, 'JSonDataBase', 'OutPuts', 'progress_report.md');
    
    if (fs.existsSync(statusFile)) {
        const content = fs.readFileSync(statusFile, 'utf8');
        
        // Parse status from progress report
        const lines = content.split('\n');
        let status = 'Ready';
        let progress = '0%';
        
        for (const line of lines) {
            if (line.includes('Overall Progress:')) {
                const match = line.match(/(\d+)%/);
                if (match) {
                    progress = match[1] + '%';
                    status = progress === '100%' ? 'Complete' : 'In Progress';
                }
            }
        }
        
        updateStatusBar(`${status} (${progress})`, `Last updated: ${new Date().toLocaleString()}`);
    } else {
        updateStatusBar('No data', 'Run auto management to see status');
    }
}

function showProjectDetails() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceFolder) return;
    
    const statusFile = path.join(workspaceFolder, 'JSonDataBase', 'OutPuts', 'progress_report.md');
    
    if (fs.existsSync(statusFile)) {
        const content = fs.readFileSync(statusFile, 'utf8');
        vscode.window.showInformationMessage('Project details opened in new editor');
        
        vscode.workspace.openTextDocument(statusFile).then(doc => {
            vscode.window.showTextDocument(doc);
        });
    } else {
        vscode.window.showWarningMessage('No progress report found. Run auto management first.');
    }
}

module.exports = {
    activate,
    deactivate
};
