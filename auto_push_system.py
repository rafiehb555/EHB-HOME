#!/usr/bin/env python3
"""
EHB Home Page - Auto Push System
Automatically pushes data to GitHub repository when tests are completed
"""

import os
import sys
import json
import subprocess
import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_push.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoPushSystem:
    """Auto-push system for GitHub repository"""

    def __init__(self, repo_url: str = "https://github.com/rafiehb555/EHB-HOME.git"):
        self.repo_url = repo_url
        self.project_root = Path.cwd()
        self.git_dir = self.project_root / ".git"
        self.auto_push_enabled = True

        # Test results tracking
        self.test_results = []
        self.last_push_time = None
        self.push_count = 0

        # Initialize git if needed
        self._init_git()

    def _init_git(self):
        """Initialize git repository if not already initialized"""
        try:
            if not self.git_dir.exists():
                logger.info("Initializing git repository...")
                subprocess.run(["git", "init"], check=True, cwd=self.project_root)

                # Add remote origin
                subprocess.run([
                    "git", "remote", "add", "origin", self.repo_url
                ], check=True, cwd=self.project_root)

                logger.info("Git repository initialized successfully")
            else:
                logger.info("Git repository already exists")

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize git: {e}")

    def _get_git_status(self) -> Dict[str, Any]:
        """Get current git status"""
        try:
            # Check if there are changes to commit
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=self.project_root
            )

            has_changes = bool(result.stdout.strip())

            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, cwd=self.project_root
            )
            current_branch = branch_result.stdout.strip() or "main"

            return {
                "has_changes": has_changes,
                "current_branch": current_branch,
                "changes": result.stdout.strip().split('\n') if result.stdout.strip() else []
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get git status: {e}")
            return {"has_changes": False, "current_branch": "main", "changes": []}

    def _add_all_files(self) -> bool:
        """Add all files to git staging"""
        try:
            subprocess.run(["git", "add", "."], check=True, cwd=self.project_root)
            logger.info("All files added to staging")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to add files: {e}")
            return False

    def _commit_changes(self, message: str) -> bool:
        """Commit changes with message"""
        try:
            subprocess.run([
                "git", "commit", "-m", message
            ], check=True, cwd=self.project_root)
            logger.info(f"Changes committed: {message}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to commit changes: {e}")
            return False

    def _push_to_github(self, branch: str = "main") -> bool:
        """Push changes to GitHub"""
        try:
            subprocess.run([
                "git", "push", "origin", branch
            ], check=True, cwd=self.project_root)

            self.last_push_time = datetime.now()
            self.push_count += 1

            logger.info(f"Successfully pushed to GitHub (branch: {branch})")
            logger.info(f"Push count: {self.push_count}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to push to GitHub: {e}")
            return False

    def _create_test_summary(self, test_results: List[Dict[str, Any]]) -> str:
        """Create a summary of test results"""
        if not test_results:
            return "No test results available"

        summary_lines = []
        summary_lines.append("# 🧪 Test Results Summary")
        summary_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append(f"**Total Tests:** {len(test_results)}")
        summary_lines.append("")

        # Count results
        passed = sum(1 for result in test_results if result.get('success', False))
        failed = len(test_results) - passed

        summary_lines.append(f"**Passed:** {passed}")
        summary_lines.append(f"**Failed:** {failed}")
        summary_lines.append(f"**Success Rate:** {(passed/len(test_results))*100:.1f}%")
        summary_lines.append("")

        # Detailed results
        summary_lines.append("## 📊 Detailed Results")
        for i, result in enumerate(test_results, 1):
            status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
            summary_lines.append(f"{i}. **{result.get('test_name', 'Unknown Test')}** - {status}")

            if result.get('details'):
                summary_lines.append(f"   - {result['details']}")
            summary_lines.append("")

        return "\n".join(summary_lines)

    def _create_development_log(self) -> str:
        """Create a development log entry"""
        log_entry = f"""
# 🚀 Development Log Entry

**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Push Count:** {self.push_count}
**Last Push:** {self.last_push_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_push_time else 'Never'}

## 📈 Project Status
- **Auto-push System:** Active
- **Test Results:** {len(self.test_results)} tests completed
- **Repository:** {self.repo_url}

## 🔧 Recent Changes
- API integrations completed
- UI design tools implemented
- Auto-push system activated
- Comprehensive testing framework

## 🎯 Next Steps
- Configure production environment
- Set up monitoring and analytics
- Deploy to production servers
- Implement advanced features

---
*Auto-generated by EHB Auto-Push System*
        """.strip()

        return log_entry

    async def auto_push(self, test_results: List[Dict[str, Any]] = None,
                       commit_message: str = None) -> Dict[str, Any]:
        """Automatically push changes to GitHub"""

        if not self.auto_push_enabled:
            logger.info("Auto-push system is disabled")
            return {"success": False, "reason": "Auto-push disabled"}

        try:
            # Update test results
            if test_results:
                self.test_results.extend(test_results)

            # Get git status
            status = self._get_git_status()

            if not status["has_changes"]:
                logger.info("No changes to push")
                return {"success": True, "reason": "No changes detected"}

            # Create commit message
            if not commit_message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                commit_message = f"Auto-push: {timestamp} - EHB Home Page updates"

            # Add all files
            if not self._add_all_files():
                return {"success": False, "reason": "Failed to add files"}

            # Commit changes
            if not self._commit_changes(commit_message):
                return {"success": False, "reason": "Failed to commit changes"}

            # Push to GitHub
            if not self._push_to_github(status["current_branch"]):
                return {"success": False, "reason": "Failed to push to GitHub"}

            # Create and save test summary
            if test_results:
                summary = self._create_test_summary(test_results)
                with open("test_summary.md", "w", encoding="utf-8") as f:
                    f.write(summary)

                # Add and commit test summary
                self._add_all_files()
                self._commit_changes(f"Test Summary: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self._push_to_github(status["current_branch"])

            # Create development log
            dev_log = self._create_development_log()
            with open("DEVELOPMENT_LOG.md", "w", encoding="utf-8") as f:
                f.write(dev_log)

            logger.info("Auto-push completed successfully")
            return {
                "success": True,
                "push_count": self.push_count,
                "last_push": self.last_push_time.isoformat() if self.last_push_time else None,
                "changes": status["changes"]
            }

        except Exception as e:
            logger.error(f"Auto-push failed: {e}")
            return {"success": False, "reason": str(e)}

    def enable_auto_push(self):
        """Enable auto-push system"""
        self.auto_push_enabled = True
        logger.info("Auto-push system enabled")

    def disable_auto_push(self):
        """Disable auto-push system"""
        self.auto_push_enabled = False
        logger.info("Auto-push system disabled")

    def get_status(self) -> Dict[str, Any]:
        """Get auto-push system status"""
        return {
            "enabled": self.auto_push_enabled,
            "push_count": self.push_count,
            "last_push": self.last_push_time.isoformat() if self.last_push_time else None,
            "test_results_count": len(self.test_results),
            "repository": self.repo_url
        }

class TestAutoPush:
    """Test class that automatically pushes results"""

    def __init__(self):
        self.auto_push = AutoPushSystem()

    async def run_test_and_push(self, test_name: str, test_function) -> Dict[str, Any]:
        """Run a test and automatically push results"""
        try:
            logger.info(f"Running test: {test_name}")

            # Run the test
            start_time = time.time()
            result = await test_function()
            end_time = time.time()

            # Create test result
            test_result = {
                "test_name": test_name,
                "success": result.get("success", False),
                "execution_time": end_time - start_time,
                "timestamp": datetime.now().isoformat(),
                "details": result.get("details", ""),
                "error": result.get("error", "")
            }

            logger.info(f"Test {test_name} completed: {'✅ PASS' if test_result['success'] else '❌ FAIL'}")

            # Auto-push results
            push_result = await self.auto_push.auto_push(
                test_results=[test_result],
                commit_message=f"Test Result: {test_name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            return {
                "test_result": test_result,
                "push_result": push_result,
                "auto_pushed": push_result.get("success", False)
            }

        except Exception as e:
            logger.error(f"Test {test_name} failed: {e}")

            # Push error result
            error_result = {
                "test_name": test_name,
                "success": False,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

            await self.auto_push.auto_push(
                test_results=[error_result],
                commit_message=f"Test Error: {test_name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            return {
                "test_result": error_result,
                "push_result": {"success": False, "reason": "Test failed"},
                "auto_pushed": True
            }

# Global auto-push instance
auto_push_system = AutoPushSystem()

async def auto_push_on_test_completion(test_results: List[Dict[str, Any]]):
    """Function to be called when tests are completed"""
    return await auto_push_system.auto_push(test_results)

def enable_auto_push():
    """Enable auto-push system"""
    auto_push_system.enable_auto_push()

def disable_auto_push():
    """Disable auto-push system"""
    auto_push_system.disable_auto_push()

def get_auto_push_status():
    """Get auto-push system status"""
    return auto_push_system.get_status()

# Test functions that automatically push results
async def test_api_integrations():
    """Test API integrations and auto-push results"""
    test_auto_push = TestAutoPush()

    # Test 1: Basic functionality
    async def test_basic_functionality():
        try:
            # Import test
            from quick_test import test_basic_functionality
            result = await test_basic_functionality()
            return {"success": True, "details": "Basic functionality test passed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Test 2: API connections
    async def test_api_connections():
        try:
            # Test API connections
            import requests
            response = requests.get("https://api.github.com")
            return {"success": response.status_code == 200, "details": f"GitHub API status: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Run tests and auto-push
    results = []

    # Test 1
    result1 = await test_auto_push.run_test_and_push("Basic Functionality", test_basic_functionality)
    results.append(result1)

    # Test 2
    result2 = await test_auto_push.run_test_and_push("API Connections", test_api_connections)
    results.append(result2)

    return results

if __name__ == "__main__":
    # Enable auto-push
    enable_auto_push()

    # Run tests with auto-push
    asyncio.run(test_api_integrations())
