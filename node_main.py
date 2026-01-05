"""
HiveMind Node Application (Enhanced)

Main entry point for the HiveMind node/client with advanced features.
"""

import asyncio
import logging
import sys

from hivemind.node.client import HiveMindClient
from hivemind.common.volume_control import VolumeController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='HiveMind Node (Enhanced)')
    parser.add_argument('--session-code', type=str,
                       help='Session code to join')
    parser.add_argument('--host', type=str, default='localhost',
                       help='Host address (default: localhost)')
    parser.add_argument('--port', type=int, default=7878,
                       help='Host port (default: 7878)')
    parser.add_argument('--volume', type=float, default=1.0,
                       help='Initial volume (0.0 to 1.0, default: 1.0)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎵 HiveMind Node (Enhanced)")
    print("=" * 60)
    
    # Get session code
    session_code = args.session_code
    if not session_code:
        session_code = input("\nEnter session code (e.g., HM-1234): ").strip()
    
    if not session_code:
        print("Error: Session code is required")
        sys.exit(1)
    
    # Get host address
    host_address = args.host
    port = args.port
    
    print("\n" + "=" * 60)
    print(f"Connecting to {host_address}:{port}")
    print(f"Session: {session_code}")
    print(f"Volume: {args.volume:.1f}")
    print("=" * 60)
    print("\nPress Ctrl+C to disconnect\n")
    
    # Create client
    client = HiveMindClient(session_code)
    
    # Set initial volume
    volume_controller = VolumeController(master_volume=args.volume)
    
    try:
        # Connect to host
        await client.connect(host_address, port)
        
        # Run main loop
        await client.run()
        
    except KeyboardInterrupt:
        print("\n\nDisconnecting...")
        await client.disconnect()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        await client.disconnect()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
