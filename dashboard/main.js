/**
 * OV Dashboard Frontend - Main JavaScript Logic
 * Handles API communication and UI updates for the Euystacio System
 */

// Configuration
const API_BASE_URL = 'http://127.0.0.1:5000';
const REFRESH_INTERVAL = 5000; // 5 seconds

// State management
let refreshTimer = null;

/**
 * Initialize the dashboard
 */
function init() {
    addLog('Dashboard initialized');
    fetchMetrics();
    startAutoRefresh();
}

/**
 * Fetch metrics from the OI backend
 */
async function fetchMetrics() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/metrics`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        updateUI(data);
        addLog('Metrics refreshed successfully');
        
    } catch (error) {
        handleError('Failed to fetch metrics', error);
    }
}

/**
 * Update UI with metrics data
 */
function updateUI(data) {
    // Update system status
    if (data.status === 'ok') {
        document.getElementById('systemStatus').textContent = 'Operational';
        document.getElementById('statusIndicator').className = 'status-indicator status-ok';
    } else {
        document.getElementById('systemStatus').textContent = 'Error';
        document.getElementById('statusIndicator').className = 'status-indicator status-error';
    }
    
    // Update system info
    if (data.system) {
        document.getElementById('systemVersion').textContent = data.system.version || '-';
        document.getElementById('systemUptime').textContent = data.system.uptime || '-';
    }
    
    // Update telemetry data
    if (data.telemetry) {
        document.getElementById('telemetryValue').textContent = data.telemetry.value.toFixed(2);
        document.getElementById('telemetryCount').textContent = data.telemetry.count;
        
        if (data.telemetry.timestamp) {
            const timestamp = new Date(data.telemetry.timestamp);
            document.getElementById('telemetryTimestamp').textContent = timestamp.toLocaleTimeString();
        }
    }
}

/**
 * Execute TFM1 command
 */
async function executeTfm1Command() {
    const button = document.getElementById('executeTfm1Btn');
    const resultDiv = document.getElementById('commandResult');
    
    try {
        // Disable button during execution
        button.disabled = true;
        button.textContent = 'Executing...';
        resultDiv.innerHTML = '';
        
        addLog('Executing TFM1 command...');
        
        const response = await fetch(`${API_BASE_URL}/api/v1/command/execute-tfm1`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                source: 'ov-dashboard',
                timestamp: new Date().toISOString()
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'success') {
            resultDiv.innerHTML = '<div style="background: #e8f5e9; color: #2e7d32; padding: 10px; border-radius: 5px; margin-top: 10px;">Command executed successfully</div>';
            addLog('TFM1 command executed successfully');
            
            // Refresh metrics to show updated telemetry
            setTimeout(fetchMetrics, 500);
        } else {
            throw new Error(data.error || 'Command execution failed');
        }
        
    } catch (error) {
        handleError('Failed to execute TFM1 command', error);
        resultDiv.innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
    } finally {
        // Re-enable button
        button.disabled = false;
        button.textContent = 'Execute TFM1';
    }
}

/**
 * Add entry to activity log
 */
function addLog(message) {
    const logEntries = document.getElementById('logEntries');
    const timestamp = new Date().toLocaleTimeString();
    
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;
    
    logEntries.appendChild(logEntry);
    
    // Auto-scroll to bottom
    logEntries.scrollTop = logEntries.scrollHeight;
    
    // Keep only last 50 entries
    while (logEntries.children.length > 50) {
        logEntries.removeChild(logEntries.firstChild);
    }
}

/**
 * Handle errors
 */
function handleError(message, error) {
    console.error(message, error);
    addLog(`ERROR: ${message} - ${error.message}`);
    
    // Update status indicator to show error
    document.getElementById('statusIndicator').className = 'status-indicator status-error';
}

/**
 * Start auto-refresh of metrics
 */
function startAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
    }
    
    refreshTimer = setInterval(fetchMetrics, REFRESH_INTERVAL);
    addLog(`Auto-refresh enabled (${REFRESH_INTERVAL / 1000}s interval)`);
}

/**
 * Stop auto-refresh
 */
function stopAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
        addLog('Auto-refresh disabled');
    }
}

// Initialize dashboard when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    stopAutoRefresh();
});
