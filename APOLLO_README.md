# Apollo Digitalis Virtualis - Deployment & Usage Guide

## Quick Start

### Option 1: Static HTML (No Backend)

1. Open `apollo-dashboard.html` directly in a modern browser:
   ```bash
   # Using Python's built-in server (recommended for local testing)
   python3 -m http.server 8080
   
   # Then open in browser
   http://localhost:8080/apollo-dashboard.html
   ```

2. For VR support, use HTTPS (required by WebXR):
   ```bash
   # Using local SSL certificate
   openssl req -new -x509 -keyout localhost.pem -out localhost.pem -days 365 -nodes
   python3 -m http.server 8080 --bind localhost
   ```

### Option 2: With Backend API

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the backend server:
   ```bash
   python oi_server.py
   ```

3. Open dashboard in browser:
   ```bash
   # Dashboard will connect to backend at http://127.0.0.1:5000
   open apollo-dashboard.html
   ```

## Browser Compatibility

### Desktop
- ✅ **Chrome 100+** (Recommended for full VR support)
- ✅ **Firefox 90+** (Good VR support)
- ⚠️ **Safari 15+** (Limited WebXR support)
- ❌ **Edge Legacy** (Not supported)

### Mobile
- ✅ **Chrome Mobile** (Android, VR/AR ready)
- ✅ **Firefox Mobile** (Android)
- ⚠️ **Safari Mobile** (iOS, limited AR)
- ✅ **Samsung Internet** (VR ready)

### VR Headsets
- ✅ **Oculus Quest 1/2/3**
- ✅ **HTC Vive**
- ✅ **Valve Index**
- ✅ **Windows Mixed Reality**
- ⚠️ **Google Cardboard** (Basic support)

## Features Overview

### 1. Euystacio Holographic Chat Interface (CIC)

**Purpose**: Command and control interface for Seedbringer governance

**How to Use**:
1. Type a command in the input field
2. Press Enter or click "Esegui Comando"
3. Read AI response in chat area

**Example Commands**:
```
Avvia analisi Terræ Nova
Status sistema
Modalità VR
Aggiorna metriche TRE
```

**Response Time**: < 2 seconds for all commands

### 2. VR/AR Immersive Mode

**Desktop VR**:
1. Click "🥽 Enter VR Mode" button (bottom left)
2. Put on VR headset
3. Use head tracking to navigate
4. Use VR controllers for interaction

**Desktop 3D Navigation** (without VR):
- **Mouse Drag**: Rotate camera
- **W/A/S/D**: Move camera (forward/left/back/right)
- **Scroll**: Zoom in/out

**Mobile AR** (Future):
1. Open dashboard on AR-capable mobile device
2. Grant camera permissions
3. Point at flat surface
4. Interact with holographic elements

### 3. TRE Thresholds Monitoring

**What are TRE Metrics?**
- **Trust (T)**: AI reliability and consistency (Target: 85-100%)
- **Responsiveness (R)**: System response speed (Target: 90-100%)
- **Efficiency (E)**: Resource optimization (Target: 75-95%)

**How to Read**:
- **Green**: Above optimal threshold
- **Yellow**: Within acceptable range
- **Red**: Below critical threshold (< 75% Trust, < 80% Resp, < 65% Eff)

**Updates**: Automatic refresh every 10 seconds

### 4. 3D Visualization

**Scene Elements**:
- **Platform**: Central holographic base
- **Pillars**: 3 colored bars representing TRE metrics
  - Cyan: Trust
  - Orange: Responsiveness
  - Green: Efficiency
- **Euystacio Hologram**: Rotating sphere with glow effect
- **Info Panel**: Floating text display

**Real-time Sync**: 2D bars and 3D pillars update simultaneously

## API Endpoints (Backend)

### GET /api/v1/apollo/tre-metrics
Get current TRE threshold values

**Response**:
```json
{
  "status": "success",
  "tre_metrics": {
    "trust": 85.0,
    "responsiveness": 92.0,
    "efficiency": 78.0,
    "last_update": "2025-11-10T23:28:24.340Z"
  }
}
```

### POST /api/v1/apollo/command/execute
Execute a Seedbringer command

**Request**:
```json
{
  "command": "Avvia analisi Terræ Nova",
  "user": "seedbringer",
  "timestamp": "2025-11-10T23:28:24.340Z"
}
```

**Response**:
```json
{
  "status": "success",
  "command": "Avvia analisi Terræ Nova",
  "message": "⚙️ Avvio analisi Terræ Nova...",
  "tre_metrics": {
    "trust": 88.0,
    "responsiveness": 94.0,
    "efficiency": 81.0
  }
}
```

### GET /api/v1/apollo/auth-status
Get authentication status

**Response**:
```json
{
  "status": "success",
  "auth_status": {
    "authenticated": true,
    "user_type": "seedbringer",
    "google_access": true
  }
}
```

### GET /api/v1/apollo/session-metrics
Get current session metrics

**Response**:
```json
{
  "status": "success",
  "session_metrics": {
    "active_sessions": 1,
    "commands_executed": 42,
    "uptime": "2:15:33",
    "data_nodes": 3
  }
}
```

### GET /api/v1/apollo/command-history?limit=50
Get command execution history

**Response**:
```json
{
  "status": "success",
  "command_history": [
    {
      "command": "Status sistema",
      "user": "seedbringer",
      "timestamp": "2025-11-10T23:28:24.340Z",
      "status": "executed"
    }
  ],
  "total_commands": 42
}
```

## Configuration

### Environment Variables

```bash
# Backend server
export DEBUG=True                    # Enable debug mode (dev only)
export PORT=5000                     # Server port
export HOST=0.0.0.0                  # Server host

# Frontend (edit apollo-dashboard.html)
const API_BASE_URL = 'http://localhost:5000';  # Backend URL
```

### Customization

**Change Theme Colors** (edit CSS in apollo-dashboard.html):
```css
:root {
    --color-bg: #0a0a1a;           /* Background */
    --color-primary: #00ffff;       /* Primary cyan */
    --color-secondary: #ffaa33;     /* Secondary orange */
    --color-accent: #ff00ff;        /* Accent magenta */
    --color-success: #00ff88;       /* Success green */
}
```

**Modify TRE Update Interval**:
```javascript
// In apollo-dashboard.html
function simulateTREUpdates() {
    setInterval(() => {
        // ...
    }, 10000);  // Change 10000 to desired milliseconds
}
```

## Deployment

### Development (Local)

```bash
# 1. Start backend
python oi_server.py

# 2. Serve frontend
python3 -m http.server 8080

# 3. Open browser
open http://localhost:8080/apollo-dashboard.html
```

### Production (Cloud)

#### Option A: Static Hosting (Netlify, Vercel, GitHub Pages)

```bash
# 1. Build static assets (no build needed, pure HTML/JS)
# 2. Deploy apollo-dashboard.html

# Example: Netlify
netlify deploy --dir=. --prod
```

#### Option B: Full Stack (Heroku, AWS, Google Cloud)

```bash
# 1. Create Procfile (already exists)
web: gunicorn oi_server:app

# 2. Deploy
git push heroku main

# 3. Set environment variables
heroku config:set DEBUG=False
```

#### Option C: Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "oi_server:app", "--bind", "0.0.0.0:5000"]
```

```bash
# Build and run
docker build -t apollo-dashboard .
docker run -p 5000:5000 apollo-dashboard
```

## Troubleshooting

### VR Mode Not Working

**Problem**: "Enter VR Mode" button doesn't activate VR

**Solutions**:
1. Ensure browser supports WebXR (use Chrome or Firefox)
2. Check VR headset is connected and recognized
3. Grant browser permissions for VR access
4. Try using HTTPS instead of HTTP
5. Verify A-Frame library loaded (check browser console)

### Chat Commands Not Responding

**Problem**: Commands typed but no response

**Solutions**:
1. Check browser console for JavaScript errors
2. Verify input field is not disabled
3. Try refreshing the page
4. If using backend, verify server is running:
   ```bash
   curl http://localhost:5000/api/v1/health
   ```

### TRE Metrics Not Updating

**Problem**: Metrics stuck at initial values

**Solutions**:
1. Check browser console for errors
2. Verify `simulateTREUpdates()` is running
3. If using backend, check API endpoint:
   ```bash
   curl http://localhost:5000/api/v1/apollo/tre-metrics
   ```

### 3D Scene Not Rendering

**Problem**: Black screen or missing 3D elements

**Solutions**:
1. Verify A-Frame loaded (check `<a-scene>` in DOM)
2. Check WebGL support in browser
3. Update graphics drivers
4. Try different browser
5. Check console for WebGL errors

### Performance Issues

**Problem**: Lag, low FPS, stuttering

**Solutions**:
1. Close other browser tabs
2. Disable browser extensions
3. Lower screen resolution
4. Use desktop instead of mobile
5. Check GPU utilization (should use dedicated GPU)

## Security Considerations

### Production Checklist

- [ ] Enable HTTPS/TLS (required for WebXR)
- [ ] Implement real Google OAuth authentication
- [ ] Add rate limiting on API endpoints
- [ ] Sanitize all user inputs (XSS prevention)
- [ ] Enable CORS only for whitelisted domains
- [ ] Add Content Security Policy (CSP) headers
- [ ] Log all command executions
- [ ] Implement session management
- [ ] Add CSRF protection
- [ ] Regular security audits

### Development Best Practices

1. **Never commit secrets** to version control
2. **Use environment variables** for configuration
3. **Validate all inputs** on both frontend and backend
4. **Keep dependencies updated** (npm audit, pip-audit)
5. **Test on multiple browsers** before deploying

## Performance Optimization

### Frontend

```javascript
// Optimize 3D rendering
AFRAME.registerComponent('performance-optimizer', {
  init: function () {
    this.el.sceneEl.setAttribute('stats', false);  // Disable stats in production
    this.el.sceneEl.setAttribute('embedded', true); // Embedded mode
  }
});
```

### Backend

```python
# Add caching for TRE metrics
from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'simple'})

@app.route('/api/v1/apollo/tre-metrics')
@cache.cached(timeout=5)  # Cache for 5 seconds
def get_tre_metrics():
    # ...
```

## Monitoring & Analytics

### Recommended Tools

1. **Lighthouse**: Performance audits
   ```bash
   lighthouse http://localhost:8080/apollo-dashboard.html
   ```

2. **Chrome DevTools**: Performance profiling
   - Performance tab: FPS, frame timing
   - Memory tab: Heap snapshots
   - Network tab: Asset loading

3. **Sentry**: Error tracking (optional)
   ```javascript
   // Add to apollo-dashboard.html
   <script src="https://browser.sentry-cdn.com/7.x.x/bundle.min.js"></script>
   <script>
     Sentry.init({ dsn: 'YOUR_DSN' });
   </script>
   ```

## Support & Documentation

- **Full Spec**: See `APOLLO_DASHBOARD_SPEC.md`
- **Test Plan**: See `TEST_PLAN.md`
- **API Reference**: Backend endpoints documented above
- **A-Frame Docs**: https://aframe.io/docs/
- **WebXR Spec**: https://www.w3.org/TR/webxr/

## License

Apollo Digitalis Virtualis © 2025 - Open Interface Project

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-10  
**Maintained By**: AI Collective (AIC)
