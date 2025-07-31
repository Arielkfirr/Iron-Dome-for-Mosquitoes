# Iron Dome for Mosquitoes - Project Summary

**Iron Dome for Mosquitoes** is a production-ready, modular system for real-time mosquito detection and prevention using AI, computer vision, and IoT.

## What's Included?

- **Phone Link Integration**: Automatic photo capture and transfer from your mobile device to the system.
- **YOLOv8 AI Detection**: Fast, accurate detection of mosquitoes and insects in images (<3s per image).
- **Modular Architecture**: Clean separation of components for detection, camera management, prevention, monitoring, database, and web interface.
- **Raspberry Pi Ready**: Optimized for edge deployment and low-power devices.
- **Comprehensive Testing**: 9/9 test phases passed, with dedicated scripts for end-to-end, photo, and integration testing.
- **Easy Setup**: One-click setup scripts, batch files, and quick start guides.
- **Web Dashboard (in progress)**: Real-time monitoring and analytics (Flask/FastAPI backend).
- **Database & Analytics**: SQLite integration for detection history and analytics.
- **Cloud Integration**: Google Drive support for backup and sharing (optional).
- **Full Documentation**: README, quick start, roadmap, demo guides, and status summaries.

## Main Modules & Scripts

- `src/` - Core system (main.py, detection, camera, prevention, monitoring, web, database, utils)
- `auto_phone_link_setup.py` - One-click Phone Link setup
- `demo_for_boss.py` - Full system demo
- `debug_phone_link_phases.py` - 9-phase testing suite
- `continue_development.py` - Automated environment and status check
- `QUICK_START_GUIDE.md` - Step-by-step setup and usage
- `CURRENT_STATUS_SUMMARY.md` - Up-to-date project status
- `PROJECT_ROADMAP_AND_GOALS.md` - Roadmap and goals

**Status:** Production Ready  
**Next Steps:** Raspberry Pi deployment, web dashboard, advanced analytics

For full details, see the [README](README.md) and [QUICK_START_GUIDE](QUICK_START_GUIDE.md).