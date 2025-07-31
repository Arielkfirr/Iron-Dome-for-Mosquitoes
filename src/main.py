#!/usr/bin/env python3
"""
Iron Dome for Mosquitoes - Main Application
Advanced AI-powered pest detection system
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from core.system_manager import SystemManager


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Iron Dome for Mosquitoes - Advanced AI-powered pest detection system"
    )
    parser.add_argument(
        "--dev", 
        action="store_true", 
        help="Run in development mode"
    )
    parser.add_argument(
        "--config", 
        type=str, 
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--log-level", 
        type=str, 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    return parser.parse_args()


def main():
    """Main application entry point."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Setup logging
        logger = setup_logger(level=args.log_level)
        logger.info("🚀 Starting Iron Dome for Mosquitoes")
        
        # Load configuration
        config = ConfigLoader(args.config).load()
        logger.info("✅ Configuration loaded successfully")
        
        # Initialize system manager
        system_manager = SystemManager(config, dev_mode=args.dev)
        logger.info("✅ System manager initialized")
        
        # Start the system
        system_manager.start()
        
    except KeyboardInterrupt:
        logger.info("🛑 System shutdown requested by user")
        if 'system_manager' in locals():
            system_manager.stop()
    except Exception as e:
        logger.error(f"❌ System error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 