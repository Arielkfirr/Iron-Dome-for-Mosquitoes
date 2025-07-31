"""
Web Interface for Iron Dome for Mosquitoes
Provides real-time monitoring dashboard and API endpoints
"""

import threading
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from loguru import logger
from utils.logger import LoggerMixin

class WebInterface(LoggerMixin):
    """Web interface for real-time monitoring and control"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.enabled = config.get('enabled', True)
        self.host = config.get('host', '127.0.0.1')
        self.port = config.get('port', 5000)
        self.debug = config.get('debug', True)
        self.auto_reload = config.get('auto_reload', True)
        
        # Flask app
        self.app = None
        self.socketio = None
        self.server_thread = None
        self.running = False
        
        # System references (will be set by system manager)
        self.system_manager = None
        self.monitoring_manager = None
        self.detection_manager = None
        
        self.logger.info(f"Web interface initialized for {self.host}:{self.port}")
    
    def initialize(self):
        """Initialize the web interface"""
        try:
            self.logger.info("Initializing web interface...")
            
            # Create Flask app
            self.app = Flask(__name__)
            CORS(self.app)
            
            # Initialize SocketIO
            self.socketio = SocketIO(self.app, cors_allowed_origins="*")
            
            # Setup routes
            self._setup_routes()
            
            # Setup SocketIO events
            self._setup_socketio_events()
            
            self.logger.info("Web interface initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize web interface: {e}")
            raise
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main dashboard page"""
            return render_template('dashboard.html')
        
        @self.app.route('/api/status')
        def api_status():
            """Get system status"""
            if self.system_manager:
                return jsonify(self.system_manager.get_status())
            return jsonify({'error': 'System manager not available'})
        
        @self.app.route('/api/health')
        def api_health():
            """Get system health"""
            if self.monitoring_manager:
                return jsonify(self.monitoring_manager.check_health())
            return jsonify({'error': 'Monitoring manager not available'})
        
        @self.app.route('/api/analytics')
        def api_analytics():
            """Get analytics data"""
            if self.monitoring_manager:
                return jsonify(self.monitoring_manager.get_analytics_summary())
            return jsonify({'error': 'Monitoring manager not available'})
        
        @self.app.route('/api/detections')
        def api_detections():
            """Get recent detections"""
            limit = request.args.get('limit', 50, type=int)
            if self.monitoring_manager:
                return jsonify(self.monitoring_manager.get_detection_history(limit))
            return jsonify({'error': 'Monitoring manager not available'})
        
        @self.app.route('/api/performance')
        def api_performance():
            """Get performance metrics"""
            if self.monitoring_manager:
                return jsonify(self.monitoring_manager.get_performance_metrics())
            return jsonify({'error': 'Monitoring manager not available'})
        
        @self.app.route('/api/control/start', methods=['POST'])
        def api_start():
            """Start the system"""
            if self.system_manager:
                try:
                    self.system_manager.run()
                    return jsonify({'status': 'success', 'message': 'System started'})
                except Exception as e:
                    return jsonify({'status': 'error', 'message': str(e)})
            return jsonify({'error': 'System manager not available'})
        
        @self.app.route('/api/control/stop', methods=['POST'])
        def api_stop():
            """Stop the system"""
            if self.system_manager:
                try:
                    self.system_manager.shutdown()
                    return jsonify({'status': 'success', 'message': 'System stopped'})
                except Exception as e:
                    return jsonify({'status': 'error', 'message': str(e)})
            return jsonify({'error': 'System manager not available'})
        
        @self.app.route('/api/config', methods=['GET', 'POST'])
        def api_config():
            """Get or update configuration"""
            if request.method == 'GET':
                if hasattr(self, 'config'):
                    return jsonify(self.config)
                return jsonify({'error': 'Configuration not available'})
            else:
                # TODO: Implement configuration update
                return jsonify({'status': 'not implemented'})
    
    def _setup_socketio_events(self):
        """Setup SocketIO event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            self.logger.info("Client connected to web interface")
            emit('status', {'message': 'Connected to Iron Dome for Mosquitoes'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            self.logger.info("Client disconnected from web interface")
        
        @self.socketio.on('request_status')
        def handle_status_request():
            """Handle status request"""
            if self.system_manager:
                emit('system_status', self.system_manager.get_status())
        
        @self.socketio.on('request_analytics')
        def handle_analytics_request():
            """Handle analytics request"""
            if self.monitoring_manager:
                emit('analytics_data', self.monitoring_manager.get_analytics_summary())
    
    def set_system_references(self, system_manager, monitoring_manager, detection_manager):
        """Set references to system components"""
        self.system_manager = system_manager
        self.monitoring_manager = monitoring_manager
        self.detection_manager = detection_manager
        self.logger.info("System references set")
    
    def broadcast_detection(self, detection_data: Dict[str, Any]):
        """Broadcast detection event to connected clients"""
        if self.socketio:
            self.socketio.emit('new_detection', detection_data)
            self.logger.info(f"Broadcasted detection: {detection_data.get('classes', [])}")
    
    def broadcast_status_update(self, status_data: Dict[str, Any]):
        """Broadcast status update to connected clients"""
        if self.socketio:
            self.socketio.emit('status_update', status_data)
    
    def _start_server(self):
        """Start the Flask server in a separate thread"""
        try:
            self.logger.info(f"Starting web server on {self.host}:{self.port}")
            
            # Run Flask app with SocketIO
            self.socketio.run(
                self.app,
                host=self.host,
                port=self.port,
                debug=self.debug,
                use_reloader=self.auto_reload,
                threaded=True
            )
            
        except Exception as e:
            self.logger.error(f"Error starting web server: {e}")
    
    def start(self):
        """Start the web interface"""
        if not self.enabled:
            self.logger.info("Web interface is disabled")
            return
        
        try:
            self.running = True
            
            # Start server in separate thread
            self.server_thread = threading.Thread(target=self._start_server, daemon=True)
            self.server_thread.start()
            
            self.logger.info("Web interface started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start web interface: {e}")
            raise
    
    def stop(self):
        """Stop the web interface"""
        self.logger.info("Stopping web interface...")
        self.running = False
        
        if self.server_thread and self.server_thread.is_alive():
            # Flask server will stop when the thread ends
            self.logger.info("Web interface stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get web interface status"""
        return {
            'enabled': self.enabled,
            'host': self.host,
            'port': self.port,
            'debug': self.debug,
            'running': self.running,
            'url': f"http://{self.host}:{self.port}" if self.running else None
        }
    
    def check_health(self) -> Dict[str, Any]:
        """Check web interface health"""
        return {
            'status': 'healthy' if self.running else 'stopped',
            'enabled': self.enabled,
            'server_running': self.running,
            'last_update': datetime.now().isoformat()
        }
    
    def shutdown(self):
        """Shutdown web interface"""
        self.logger.info("Shutting down web interface...")
        self.stop()
        self.logger.info("Web interface shutdown complete") 