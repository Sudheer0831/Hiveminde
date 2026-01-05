"""
HiveMind Host Application (Enhanced)

Main entry point for the HiveMind host with advanced features.
"""

import asyncio
import logging
import sys
import time
import threading

from hivemind.host.session_manager import SessionManager
from hivemind.host.clock_sync import ClockSyncService
from hivemind.host.audio_scheduler import AudioScheduler
from hivemind.host.network_server import NetworkServer
from hivemind.host.audio_capture import AudioCapture
from hivemind.host.web_dashboard import WebDashboard
from hivemind.common.protocol import Protocol, MessageType
from hivemind.common.audio_codec import AudioCodecManager
from hivemind.common.volume_control import VolumeController
from hivemind.common.latency_calibration import LatencyCalibrator
from hivemind.config import DEFAULT_PORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HiveMindHostEnhanced:
    """Enhanced HiveMind host with advanced features."""
    
    def __init__(self, port: int = DEFAULT_PORT, 
                 enable_compression: bool = True,
                 enable_web_dashboard: bool = True,
                 web_port: int = 5000):
        """
        Initialize enhanced HiveMind host.
        
        Args:
            port: Network port
            enable_compression: Enable Opus compression
            enable_web_dashboard: Enable web dashboard
            web_port: Web dashboard port
        """
        self.port = port
        self.session_manager = SessionManager()
        self.clock_sync = ClockSyncService()
        self.audio_scheduler = AudioScheduler()
        self.network_server = NetworkServer(port=port)
        self.audio_capture = AudioCapture()
        
        # Advanced features
        self.codec_manager = AudioCodecManager(use_compression=enable_compression)
        self.volume_controller = VolumeController()
        self.latency_calibrator = LatencyCalibrator()
        
        # Web dashboard
        self.web_dashboard = None
        if enable_web_dashboard:
            self.web_dashboard = WebDashboard(self, port=web_port)
        
        self.running = False
        
        # Register message handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register network message handlers."""
        self.network_server.register_handler(
            MessageType.JOIN_REQUEST,
            self._handle_join_request
        )
        self.network_server.register_handler(
            MessageType.TIME_SYNC_REQUEST,
            self._handle_time_sync_request
        )
        self.network_server.register_handler(
            MessageType.HEARTBEAT,
            self._handle_heartbeat
        )
    
    async def _handle_join_request(self, client, payload: dict, audio_data):
        """Handle join request from a node."""
        device_id = payload['device_id']
        device_name = payload['device_name']
        session_code = payload['session_code']
        metadata = payload['metadata']
        
        logger.info(f"Join request from {device_name} ({device_id})")
        
        # Validate session code
        if session_code != self.session_manager.session_code:
            logger.warning(f"Invalid session code: {session_code}")
            response = Protocol.create_join_reject("Invalid session code")
            await client.send_message(response)
            return
        
        # Accept node
        if self.session_manager.accept_node(device_id, device_name, metadata):
            logger.info(f"Accepted node: {device_name}")
            
            # Mark client as authenticated
            client.device_id = device_id
            client.authenticated = True
            
            # Add to server's client list
            self.network_server.clients[device_id] = client
            
            # Calibrate latency (async)
            asyncio.create_task(self._calibrate_node_latency(device_id))
            
            # Send accept response
            session_info = self.session_manager.get_session_info()
            response = Protocol.create_join_accept(device_id, session_info)
            await client.send_message(response)
        else:
            logger.warning(f"Rejected node: {device_name}")
            response = Protocol.create_join_reject("Session full or invalid device")
            await client.send_message(response)
    
    async def _calibrate_node_latency(self, device_id: str):
        """Calibrate latency for a node."""
        await asyncio.sleep(2)  # Wait for node to stabilize
        latency = self.latency_calibrator.calibrate(device_id)
        logger.info(f"Calibrated {device_id}: {latency:.2f}ms")
    
    async def _handle_time_sync_request(self, client, payload: dict, audio_data):
        """Handle time sync request from a node."""
        if not client.authenticated:
            return
        
        client_time = payload['client_time']
        
        # Get sync response
        sync_data = self.clock_sync.handle_sync_request(
            client.device_id,
            client_time
        )
        
        # Send response
        response = Protocol.create_time_sync_response(
            host_time=sync_data['host_time'],
            client_time=client_time
        )
        await client.send_message(response)
    
    async def _handle_heartbeat(self, client, payload: dict, audio_data):
        """Handle heartbeat from a node."""
        if not client.authenticated:
            return
        
        device_id = payload['device_id']
        self.session_manager.update_heartbeat(device_id)
        
        # Send ack
        response = Protocol.create_heartbeat_ack(device_id)
        await client.send_message(response)
    
    async def _audio_distribution_loop(self):
        """Distribute captured audio to all nodes."""
        logger.info("Starting audio distribution")
        
        while self.running:
            # Get captured audio chunk
            audio_chunk = self.audio_capture.get_chunk(timeout=0.1)
            
            if audio_chunk is None:
                continue
            
            # Apply volume control
            audio_chunk = self.volume_controller.apply_volume(audio_chunk)
            
            # Schedule the chunk
            schedule_info = self.audio_scheduler.schedule_chunk(audio_chunk)
            
            # Encode audio (with compression if enabled)
            audio_bytes, is_compressed = self.codec_manager.encode(audio_chunk)
            
            # Create audio chunk message
            message = Protocol.create_audio_chunk(
                play_at=schedule_info['play_at'],
                sample_rate=schedule_info['sample_rate'],
                channels=schedule_info['channels'],
                audio_data=audio_bytes
            )
            
            # Broadcast to all nodes
            await self.network_server.broadcast(message)
    
    async def _monitoring_loop(self):
        """Monitor session health."""
        while self.running:
            await asyncio.sleep(10.0)
            
            # Check for stale nodes
            stale_nodes = self.session_manager.check_stale_nodes()
            for device_id in stale_nodes:
                logger.warning(f"Removing stale node: {device_id}")
                self.session_manager.remove_node(device_id)
                if device_id in self.network_server.clients:
                    del self.network_server.clients[device_id]
            
            # Log status
            node_count = len(self.session_manager.nodes)
            logger.info(f"Session status: {node_count} nodes connected")
    
    def _start_web_dashboard(self):
        """Start web dashboard in separate thread."""
        if self.web_dashboard:
            dashboard_thread = threading.Thread(
                target=self.web_dashboard.run,
                daemon=True
            )
            dashboard_thread.start()
            logger.info(f"Web dashboard available at http://localhost:5000")
    
    async def start(self):
        """Start the host."""
        self.running = True
        
        print("=" * 60)
        print("🎵 HiveMind Host (Enhanced)")
        print("=" * 60)
        print(f"Session Code: {self.session_manager.session_code}")
        print(f"Network Port: {self.port}")
        print(f"Compression: {'Enabled (Opus)' if self.codec_manager.use_compression else 'Disabled'}")
        if self.web_dashboard:
            print(f"Web Dashboard: http://localhost:5000")
        print("=" * 60)
        print("\nWaiting for nodes to join...")
        print("Press Ctrl+C to stop\n")
        
        # Start web dashboard
        self._start_web_dashboard()
        
        # Start audio capture
        self.audio_capture.start()
        
        # Start background tasks
        asyncio.create_task(self._audio_distribution_loop())
        asyncio.create_task(self._monitoring_loop())
        
        # Start network server (this blocks)
        await self.network_server.start()
    
    async def stop(self):
        """Stop the host."""
        logger.info("Stopping host...")
        self.running = False
        
        # Stop audio capture
        self.audio_capture.stop()
        
        # Stop network server
        await self.network_server.stop()
        
        logger.info("Host stopped")


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='HiveMind Host (Enhanced)')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT,
                       help='Network port (default: 7878)')
    parser.add_argument('--no-compression', action='store_true',
                       help='Disable audio compression')
    parser.add_argument('--no-web', action='store_true',
                       help='Disable web dashboard')
    parser.add_argument('--web-port', type=int, default=5000,
                       help='Web dashboard port (default: 5000)')
    
    args = parser.parse_args()
    
    host = HiveMindHostEnhanced(
        port=args.port,
        enable_compression=not args.no_compression,
        enable_web_dashboard=not args.no_web,
        web_port=args.web_port
    )
    
    try:
        await host.start()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        await host.stop()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        await host.stop()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
