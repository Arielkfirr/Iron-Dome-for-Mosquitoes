#!/usr/bin/env python3
"""
GitHub Repository Setup Script for Iron Dome Mosquitoes Project
This script helps set up the GitHub remote repository.
"""

import os
import subprocess
import sys

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 Iron Dome Mosquitoes - GitHub Repository Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists(".git"):
        print("❌ Error: Not in a git repository. Please run this from the IronDomeMosquitoes directory.")
        return
    
    print("✅ Git repository found")
    
    # Check current status
    success, stdout, stderr = run_command('"C:\\Program Files\\Git\\bin\\git.exe" status --porcelain')
    if success and not stdout.strip():
        print("✅ Working directory is clean")
    else:
        print("⚠️  There are uncommitted changes. Please commit them first.")
        return
    
    print("\n📋 Next Steps:")
    print("1. Go to https://github.com/new")
    print("2. Create a new repository named 'IronDomeMosquitoes'")
    print("3. Make it PUBLIC (for easier sharing)")
    print("4. DO NOT initialize with README, .gitignore, or license")
    print("5. Copy the repository URL")
    
    print("\n🔗 After creating the repository, run these commands:")
    print('git remote add origin https://github.com/YOUR_USERNAME/IronDomeMosquitoes.git')
    print('git branch -M main')
    print('git push -u origin main')
    
    print("\n📝 Repository Description:")
    print("Iron Dome for Mosquitoes - AI-powered mosquito detection and prevention system")
    print("using computer vision and automated prevention mechanisms.")
    
    print("\n🏷️  Suggested Topics:")
    print("- computer-vision")
    print("- mosquito-detection")
    print("- ai-prevention")
    print("- raspberry-pi")
    print("- python")
    print("- yolo")
    print("- automation")
    
    print("\n📄 Key Files to Highlight:")
    print("- README.md - Main project documentation")
    print("- BOSS_DEMO_GUIDE.md - Demo instructions")
    print("- EXECUTIVE_SUMMARY.md - Project overview")
    print("- requirements.txt - Dependencies")
    print("- src/ - Main source code")
    
    print("\n🎯 Ready to push to GitHub!")
    print("After setting up the remote, you can run:")
    print('git push -u origin main')

if __name__ == "__main__":
    main() 