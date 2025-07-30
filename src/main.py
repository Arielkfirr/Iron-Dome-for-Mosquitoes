#!/usr/bin/env python3
"""
Iron Dome for Mosquitoes - Main Application
Main entry point for the mosquito detection and prevention system
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from core.system_manager import SystemManager
from utils.logger import setup_logger
from utils.config_loader import ConfigLoader

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Iron Dome for Mosquitoes - Advanced Mosquito Detection System"
    )
    
    parser.add_argument(
        "--dev", 
        action="store_true", 
        help="Run in development mode"
    )
    
    parser.add_argument(
        "--production", 
        action="store_true", 
        help="Run in production mode"
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
    """Main application entry point"""
    print("🦟🛡️ Iron Dome for Mosquitoes")
    print("=" * 50)
    
    # Parse arguments
    args = parse_arguments()
    
    try:
        # Setup logging
        logger = setup_logger(level=args.log_level)
        logger.info("Starting Iron Dome for Mosquitoes system")
        
        # Load configuration
        config_loader = ConfigLoader(args.config)
        config = config_loader.load()
        logger.info("Configuration loaded successfully")
        
        # Determine mode
        if args.dev:
            mode = "development"
            logger.info("Running in development mode")
        elif args.production:
            mode = "production"
            logger.info("Running in production mode")
        else:
            mode = "default"
            logger.info("Running in default mode")
        
        # Initialize system manager
        system_manager = SystemManager(config, mode)
        
        # Start the system
        logger.info("Initializing system components...")
        system_manager.initialize()
        
        # Run the system
        logger.info("Starting system...")
        system_manager.run()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Iron Dome for Mosquitoes...")
        if 'system_manager' in locals():
            system_manager.shutdown()
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if 'logger' in locals():
            logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 