"""
OI Backend Server for Euystacio System
Flask-based API server providing metrics and command endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import yaml
import os

app = Flask(__name__)
CORS(app)

# Global telemetry data storage
telemetry_data = {
    "value": 0.00,
    "timestamp": None,
    "count": 0
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
