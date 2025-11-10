"""
OI Backend Server for Euystacio System
Flask-based API server providing metrics and command endpoints
Enhanced for Apollo Digitalis Virtualis Dashboard
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import yaml
import os
import random

app = Flask(__name__)
CORS(app)

# Global telemetry data storage
telemetry_data = {
    "value": 0.00,
    "timestamp": None,
    "count": 0
}

# Apollo Dashboard - TRE Thresholds and Command History
apollo_data = {
    "tre_metrics": {
        "trust": 85.0,
        "responsiveness": 92.0,
        "efficiency": 78.0,
        "last_update": None
    },
    "command_history": [],
    "auth_status": {
        "authenticated": True,
        "user_type": "seedbringer",
        "google_access": True
    },
    "session_metrics": {
        "active_sessions": 1,
        "commands_executed": 0,
        "uptime_start": datetime.now(),
        "data_nodes": 3
    }
}

# Load financial endpoints configuration
def load_financial_config():
    config_path = os.path.join('configuration', 'financial_endpoints.yaml')
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None


@app.route('/api/v1/metrics', methods=['GET'])
def get_metrics():
    """
    Endpoint to retrieve telemetry data and metrics
    Tracks 0.00 telemetry data and metrics
    """
    telemetry_data['timestamp'] = datetime.now().isoformat()
    
    metrics = {
        'status': 'ok',
        'telemetry': {
            'value': telemetry_data['value'],
            'timestamp': telemetry_data['timestamp'],
            'count': telemetry_data['count']
        },
        'system': {
            'uptime': 'active',
            'version': '1.0.0'
        }
    }
    
    return jsonify(metrics), 200


@app.route('/api/v1/command/execute-tfm1', methods=['POST'])
def execute_tfm1():
    """
    Command endpoint to execute TFM1 operations
    """
    try:
        data = request.get_json() or {}
        
        # Update telemetry count
        telemetry_data['count'] += 1
        telemetry_data['timestamp'] = datetime.now().isoformat()
        
        response = {
            'status': 'success',
            'command': 'execute-tfm1',
            'timestamp': telemetry_data['timestamp'],
            'parameters': data,
            'result': {
                'executed': True,
                'telemetry_updated': True
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        # Log the full error but don't expose stack trace to user
        app.logger.error(f"Error executing TFM1: {str(e)}")
        return jsonify({
            'status': 'error',
            'command': 'execute-tfm1',
            'error': 'Command execution failed'
        }), 500


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/v1/apollo/tre-metrics', methods=['GET'])
def get_tre_metrics():
    """
    Get TRE (Trust, Responsiveness, Efficiency) threshold metrics
    """
    apollo_data['tre_metrics']['last_update'] = datetime.now().isoformat()
    
    return jsonify({
        'status': 'success',
        'tre_metrics': apollo_data['tre_metrics']
    }), 200


@app.route('/api/v1/apollo/tre-metrics', methods=['POST'])
def update_tre_metrics():
    """
    Update TRE metrics (typically called after command execution)
    """
    try:
        data = request.get_json() or {}
        
        # Validate and update TRE metrics
        if 'trust' in data:
            apollo_data['tre_metrics']['trust'] = max(0, min(100, float(data['trust'])))
        if 'responsiveness' in data:
            apollo_data['tre_metrics']['responsiveness'] = max(0, min(100, float(data['responsiveness'])))
        if 'efficiency' in data:
            apollo_data['tre_metrics']['efficiency'] = max(0, min(100, float(data['efficiency'])))
        
        apollo_data['tre_metrics']['last_update'] = datetime.now().isoformat()
        
        return jsonify({
            'status': 'success',
            'tre_metrics': apollo_data['tre_metrics']
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error updating TRE metrics: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to update TRE metrics'
        }), 500


@app.route('/api/v1/apollo/command/execute', methods=['POST'])
def execute_apollo_command():
    """
    Execute executive command from Euystacio Chat Interface
    """
    try:
        data = request.get_json() or {}
        command = data.get('command', '').strip()
        user = data.get('user', 'unknown')
        
        if not command:
            return jsonify({
                'status': 'error',
                'error': 'Command cannot be empty'
            }), 400
        
        # Validate authentication (simplified for MVP)
        if apollo_data['auth_status']['user_type'] != 'seedbringer':
            return jsonify({
                'status': 'error',
                'error': 'Unauthorized - Seedbringer access required'
            }), 403
        
        # Process command
        command_lower = command.lower()
        timestamp = datetime.now().isoformat()
        
        # Increment command counter
        apollo_data['session_metrics']['commands_executed'] += 1
        
        # Command processing logic
        response = {
            'status': 'success',
            'command': command,
            'timestamp': timestamp,
            'user': user
        }
        
        if 'analisi' in command_lower or 'terræ nova' in command_lower:
            # Simulate Terræ Nova analysis
            response['message'] = '⚙️ Avvio analisi Terræ Nova... Sistema GGC attivato.'
            response['analysis_result'] = 'Analisi completata con successo.'
            
            # Update TRE metrics with analysis results
            apollo_data['tre_metrics']['trust'] = 88.0 + random.uniform(-2, 2)
            apollo_data['tre_metrics']['responsiveness'] = 94.0 + random.uniform(-2, 2)
            apollo_data['tre_metrics']['efficiency'] = 81.0 + random.uniform(-2, 2)
            apollo_data['tre_metrics']['last_update'] = timestamp
            
            response['tre_metrics'] = apollo_data['tre_metrics']
            
        elif 'status' in command_lower or 'stato' in command_lower:
            # Return system status
            uptime = datetime.now() - apollo_data['session_metrics']['uptime_start']
            response['message'] = '📊 Stato Sistema: OPERATIVO'
            response['system_status'] = {
                'active_sessions': apollo_data['session_metrics']['active_sessions'],
                'commands_executed': apollo_data['session_metrics']['commands_executed'],
                'uptime': str(uptime).split('.')[0],  # Remove microseconds
                'vr_ar_available': True,
                'aic_connection': 'stable'
            }
            
        elif 'vr' in command_lower or 'ar' in command_lower:
            # VR/AR mode information
            response['message'] = '🥽 Modalità VR/AR pronta. Sistema immersivo disponibile.'
            response['vr_ar_status'] = {
                'vr_available': True,
                'ar_available': False,  # Future implementation
                'recommended_browser': 'Chrome, Firefox'
            }
            
        elif 'euystacio' in command_lower:
            # Euystacio AI information
            response['message'] = '👋 Euystacio AI è online. Sistema olografico operativo.'
            response['euystacio_status'] = 'online'
            
        else:
            # Generic command execution
            response['message'] = f'🔄 Comando ricevuto: "{command}". Elaborazione tramite AIC...'
            response['processing'] = True
        
        # Log command to history
        command_entry = {
            'command': command,
            'user': user,
            'timestamp': timestamp,
            'status': 'executed'
        }
        apollo_data['command_history'].append(command_entry)
        
        # Keep only last 100 commands
        if len(apollo_data['command_history']) > 100:
            apollo_data['command_history'] = apollo_data['command_history'][-100:]
        
        return jsonify(response), 200
    
    except Exception as e:
        app.logger.error(f"Error executing Apollo command: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Command execution failed',
            'details': str(e)
        }), 500


@app.route('/api/v1/apollo/auth-status', methods=['GET'])
def get_auth_status():
    """
    Get authentication status for Seedbringer access
    """
    return jsonify({
        'status': 'success',
        'auth_status': apollo_data['auth_status']
    }), 200


@app.route('/api/v1/apollo/session-metrics', methods=['GET'])
def get_session_metrics():
    """
    Get current session metrics
    """
    uptime = datetime.now() - apollo_data['session_metrics']['uptime_start']
    
    metrics = {
        'active_sessions': apollo_data['session_metrics']['active_sessions'],
        'commands_executed': apollo_data['session_metrics']['commands_executed'],
        'uptime': str(uptime).split('.')[0],
        'data_nodes': apollo_data['session_metrics']['data_nodes']
    }
    
    return jsonify({
        'status': 'success',
        'session_metrics': metrics
    }), 200


@app.route('/api/v1/apollo/command-history', methods=['GET'])
def get_command_history():
    """
    Get command execution history
    """
    limit = request.args.get('limit', 50, type=int)
    
    return jsonify({
        'status': 'success',
        'command_history': apollo_data['command_history'][-limit:],
        'total_commands': len(apollo_data['command_history'])
    }), 200


if __name__ == '__main__':
    # Load configuration
    config = load_financial_config()
    if config:
        print("Financial configuration loaded successfully")
    else:
        print("Warning: Financial configuration not found")
    
    # Start server
    # Note: Debug mode is enabled for development only
    # For production deployment, set DEBUG=False and use a production WSGI server
    debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
    print("Starting OI Server on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
