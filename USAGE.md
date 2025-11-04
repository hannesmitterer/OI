# OI - Open Interface

Open Interface for the Euystacio System - integrating OI Backend and OV Frontend modules.

## Overview

This package provides a cohesive integration of:
- **OI Backend**: Python Flask server providing REST API endpoints for metrics and command execution
- **OV Frontend**: Web-based dashboard for system visualization and control

## Components

### OI Backend (`oi_server.py`)

Flask-based REST API server providing:

- **GET /api/v1/metrics** - Retrieve telemetry data and system metrics
- **POST /api/v1/command/execute-tfm1** - Execute TFM1 command
- **GET /api/v1/health** - Health check endpoint

### Configuration (`configuration/financial_endpoints.yaml`)

YAML configuration file defining:
- Financial endpoint settings
- Telemetry configuration (initial value: 0.00)
- Command execution parameters
- System-level settings

### OV Dashboard (`dashboard/`)

Web-based dashboard providing:
- Real-time system status monitoring
- Telemetry data visualization
- Command execution interface
- Activity logging
- Auto-refresh functionality (5-second interval)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the OI Backend Server

```bash
python3 oi_server.py
```

The server will start on `http://127.0.0.1:5000`

**Environment Variables:**
- `DEBUG` - Enable/disable debug mode (default: `True`)
  - Set to `False` for production: `DEBUG=False python3 oi_server.py`

### Accessing the OV Dashboard

1. Start a simple HTTP server in the dashboard directory:
```bash
cd dashboard
python3 -m http.server 8080
```

2. Open your browser to: `http://127.0.0.1:8080/index.html`

## API Examples

### Get Metrics

```bash
curl http://127.0.0.1:5000/api/v1/metrics
```

Response:
```json
{
  "status": "ok",
  "telemetry": {
    "value": 0.00,
    "timestamp": "2025-11-04T06:23:05.062387",
    "count": 0
  },
  "system": {
    "uptime": "active",
    "version": "1.0.0"
  }
}
```

### Execute TFM1 Command

```bash
curl -X POST http://127.0.0.1:5000/api/v1/command/execute-tfm1 \
  -H "Content-Type: application/json" \
  -d '{"source": "cli"}'
```

Response:
```json
{
  "status": "success",
  "command": "execute-tfm1",
  "timestamp": "2025-11-04T06:23:12.679979",
  "result": {
    "executed": true,
    "telemetry_updated": true
  }
}
```

## Features

- ✅ REST API for metrics and command execution
- ✅ Telemetry tracking (0.00 initial value)
- ✅ Real-time dashboard with auto-refresh
- ✅ CORS enabled for cross-origin requests
- ✅ Configuration-based setup
- ✅ Security hardened (no debug mode in production)
- ✅ Error sanitization (no stack trace exposure)

## Security

- Debug mode is configurable via environment variable
- Error messages are sanitized to prevent information disclosure
- All dependencies verified against GitHub Advisory Database
- CodeQL security analysis passed

## Production Deployment

For production use:

1. Disable debug mode:
```bash
DEBUG=False python3 oi_server.py
```

2. Use a production WSGI server (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 oi_server:app
```

## License

See repository license file.
