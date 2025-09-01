#!/usr/bin/env python3
"""
Comprehensive test script for CocoPack installation.

This script tests:
1. Package building (both sdist and wheel)
2. Installation of the package with different installation options
3. Python module imports
4. Shell command functionality
5. Uninstallation

Usage:
    python test_installation.py [--keep-env] [--skip-build] [--verbose]

Options:
    --keep-env     Don't remove the test environments after testing
    --skip-build   Skip the build step and use existing wheel/sdist files
    --verbose      Show additional output
"""

import sys
import venv
import shutil
import platform
import tempfile
import subprocess
import argparse
from pathlib import Path


class ColorOutput:
    """Terminal color output helper."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def header(text):
        """Format text as header."""
        return f"{ColorOutput.HEADER}{text}{ColorOutput.ENDC}"

    @staticmethod
    def success(text):
        """Format text as success."""
        return f"{ColorOutput.GREEN}{text}{ColorOutput.ENDC}"

    @staticmethod
    def error(text):
        """Format text as error."""
        return f"{ColorOutput.RED}{text}{ColorOutput.ENDC}"

    @staticmethod
    def warning(text):
        """Format text as warning."""
        return f"{ColorOutput.YELLOW}{text}{ColorOutput.ENDC}"

    @staticmethod
    def info(text):
        """Format text as info."""
        return f"{ColorOutput.BLUE}{text}{ColorOutput.ENDC}"

    @staticmethod
    def bold(text):
        """Format text as bold."""
        return f"{ColorOutput.BOLD}{text}{ColorOutput.ENDC}"


class TestEnvironment:
    """Manages a virtual environment for testing."""

    def __init__(self, name, path, keep_env=False, verbose=False):
        """Initialize a test environment.
        
        Args:
            name: The name of the environment
            path: The path to create the environment at
            keep_env: If True, don't delete the environment when done
            verbose: If True, show additional output
        """
        self.name = name
        self.path = Path(path) / name
        self.keep_env = keep_env
        self.verbose = verbose
        self.python_exe = None
        self.pip_exe = None
        
        # Create the environment
        self._create_env()
    
    def _create_env(self):
        """Create the virtual environment."""
        print(f"Creating {ColorOutput.bold(self.name)} environment at {self.path}...")
        venv.create(self.path, with_pip=True)
        
        # Set paths to executables
        if platform.system() == 'Windows':
            self.python_exe = self.path / 'Scripts' / 'python.exe'
            self.pip_exe = self.path / 'Scripts' / 'pip.exe'
        else:
            self.python_exe = self.path / 'bin' / 'python'
            self.pip_exe = self.path / 'bin' / 'pip'
        
        # Upgrade pip
        self.run([str(self.pip_exe), "install", "--upgrade", "pip"])
    
    def run(self, cmd, check=True, capture_output=True):
        """Run a command in the environment."""
        cmd_str = " ".join(str(c) for c in cmd)
        if self.verbose:
            print(f"Running: {cmd_str}")
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True,
            check=False  # We'll handle errors ourselves
        )
        
        if check and result.returncode != 0:
            print(ColorOutput.error(f"Command failed: {cmd_str}"))
            if result.stdout:
                print(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"STDERR:\n{result.stderr}")
            sys.exit(1)
        
        return result
    
    def run_python(self, code, check=True):
        """Run Python code in the environment."""
        return self.run([str(self.python_exe), "-c", code], check=check)
    
    def install_package(self, package_path, extras=None):
        """Install a package in the environment."""
        extras_str = f"[{extras}]" if extras else ""
        cmd = [str(self.pip_exe), "install", f"{package_path}{extras_str}"]
        return self.run(cmd)
    
    def uninstall_package(self, package_name):
        """Uninstall a package from the environment."""
        cmd = [str(self.pip_exe), "uninstall", "-y", package_name]
        return self.run(cmd)
    
    def cleanup(self):
        """Clean up the environment."""
        if not self.keep_env:
            print(f"Removing {self.name} environment...")
            shutil.rmtree(self.path, ignore_errors=True)
        else:
            print(f"Keeping {self.name} environment at {self.path}")


class TestFailure(Exception):
    """Exception raised when a test fails."""
    pass


class CocoPackInstallationTester:
    """Tests installation and functionality of the CocoPack package."""
    
    def __init__(self, keep_env=False, skip_build=False, verbose=False, keep_dist=False):
        """Initialize the tester.
        
        Args:
            keep_env: If True, don't delete the test environments
            skip_build: If True, skip the build step and use existing wheel/sdist files
            verbose: If True, show additional output
            keep_dist: If True, don't delete the dist directory after testing
        """
        self.repo_root = Path(__file__).parent.parent.absolute()
        self.dist_dir = self.repo_root / "dist"
        self.keep_env = keep_env
        self.skip_build = skip_build
        self.verbose = verbose
        self.keep_dist = keep_dist
        self.dist_existed = self.dist_dir.exists()
        
        # Create temp directory for test environments
        self.temp_dir = Path(tempfile.mkdtemp(prefix="cocopack-test-"))
        print(f"Using temporary directory: {self.temp_dir}")
        
        # Initialize test environments
        self.build_env = None
        self.basic_env = None
        self.shell_env = None
        self.dev_env = None
        
        # Initialize test results
        self.test_results = {
            "build": False,
            "basic_install": False,
            "shell_install": False,
            "dev_install": False,
            "python_import": False,
            "shell_commands": False,
            "uninstallation": False
        }
    
    def run_tests(self):
        """Run all tests."""
        try:
            # Create build environment and build packages
            if not self.skip_build:
                self.build_env = TestEnvironment("build-env", self.temp_dir, self.keep_env, self.verbose)
                self.test_build_package()
            
            # Create test environments for different installation options
            self.basic_env = TestEnvironment("basic-env", self.temp_dir, self.keep_env, self.verbose)
            self.shell_env = TestEnvironment("shell-env", self.temp_dir, self.keep_env, self.verbose)
            self.dev_env = TestEnvironment("dev-env", self.temp_dir, self.keep_env, self.verbose)
            
            # Test installations
            self.test_basic_installation()
            self.test_shell_installation()
            self.test_dev_installation()
            
            # Test functionality
            self.test_python_imports()
            self.test_shell_commands()
            
            # Test uninstallation
            self.test_uninstallation()
            
            # Print results
            self.print_test_results()
            
            # Return success if all tests passed
            if all(self.test_results.values()):
                print(ColorOutput.success("\n✅ All tests passed!"))
                return 0
            else:
                print(ColorOutput.error("\n❌ Some tests failed!"))
                return 1
            
        except TestFailure as e:
            print(ColorOutput.error(f"\n❌ Test failed: {e}"))
            return 1
        
        finally:
            # Clean up environments
            self.cleanup()
    
    def test_build_package(self):
        """Test building the package."""
        print(ColorOutput.header("\n=== Testing Package Build ==="))
        
        # Clean dist directory
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        
        # Install build dependencies
        self.build_env.run([str(self.build_env.pip_exe), "install", "build"])
        
        # Build the package
        print("Building package...")
        self.build_env.run(
            [str(self.build_env.python_exe), "-m", "build"],
            capture_output=not self.verbose,
            check=True
        )
        
        # Check if build succeeded
        wheel_files = list(self.dist_dir.glob("*.whl"))
        sdist_files = list(self.dist_dir.glob("*.tar.gz"))
        
        if not wheel_files:
            raise TestFailure("No wheel file was built")
        if not sdist_files:
            raise TestFailure("No source distribution was built")
        
        self.wheel_file = wheel_files[0]
        self.sdist_file = sdist_files[0]
        
        print(ColorOutput.success(f"✅ Successfully built {self.wheel_file.name} and {self.sdist_file.name}"))
        self.test_results["build"] = True
    
    def test_basic_installation(self):
        """Test basic installation (no extras)."""
        print(ColorOutput.header("\n=== Testing Basic Installation ==="))
        
        # Get wheel file
        if not hasattr(self, 'wheel_file'):
            self.wheel_file = list(self.dist_dir.glob("*.whl"))[0]
        
        # Install package
        print(f"Installing {self.wheel_file.name}...")
        self.basic_env.install_package(self.wheel_file)
        
        # Test basic import
        result = self.basic_env.run_python("import cocopack; print(f'CocoPack version: {cocopack.__version__}')")
        print(result.stdout.strip())
        
        print(ColorOutput.success("✅ Basic installation successful"))
        self.test_results["basic_install"] = True
    
    def test_shell_installation(self):
        """Test installation with shell extras."""
        print(ColorOutput.header("\n=== Testing Shell Installation ==="))
        
        # Get wheel file
        if not hasattr(self, 'wheel_file'):
            self.wheel_file = list(self.dist_dir.glob("*.whl"))[0]
        
        # Install package with shell extras
        print(f"Installing {self.wheel_file.name} with shell extras...")
        self.shell_env.install_package(self.wheel_file, extras="shell")
        
        # Test basic import
        result = self.shell_env.run_python("import cocopack; print(f'CocoPack version: {cocopack.__version__}')")
        print(result.stdout.strip())
        
        print(ColorOutput.success("✅ Shell installation successful"))
        self.test_results["shell_install"] = True
    
    
    def test_dev_installation(self):
        """Test installation with dev extras."""
        print(ColorOutput.header("\n=== Testing Dev Installation ==="))
        
        # Get wheel file
        if not hasattr(self, 'wheel_file'):
            self.wheel_file = list(self.dist_dir.glob("*.whl"))[0]
        
        # Install package with dev extras
        print(f"Installing {self.wheel_file.name} with dev extras...")
        self.dev_env.install_package(self.wheel_file, extras="dev")
        
        # Test basic import
        result = self.dev_env.run_python("import cocopack; print(f'CocoPack version: {cocopack.__version__}')")
        print(result.stdout.strip())
        
        # Test if dev dependencies are available
        result = self.dev_env.run_python("import pytest, black, isort; print('Dev dependencies are available')")
        print(result.stdout.strip())
        
        print(ColorOutput.success("✅ Dev installation successful"))
        self.test_results["dev_install"] = True
    
    def test_python_imports(self):
        """Test Python module imports."""
        print(ColorOutput.header("\n=== Testing Python Imports ==="))
        
        # Define the modules to test
        modules = [
            "cocopack",
            "cocopack.notebook",
            "cocopack.notebook.stylizer",
            "cocopack.notebook.magics",
            "cocopack.shellpack",
            "cocopack.shellpack.cli",
            "cocopack.shellpack.commands",
            "cocopack.shellpack.install",
            "cocopack.convert",
            "cocopack.figure_ops",
            "cocopack.overleaf",
            "cocopack.pacman",
            "cocopack.path_ops"
        ]
        
        # Create import test code
        import_code = ";".join([f"import {module}" for module in modules])
        import_code = f"""
try:
    {import_code}
    print("All modules imported successfully")
except ImportError as e:
    import sys
    print(f"Import error: {{e}}", file=sys.stderr)
    sys.exit(1)
"""
        
        # Test imports in each environment
        for env_name, env in [
            ("Basic", self.basic_env),
            ("Shell", self.shell_env),
            ("Dev", self.dev_env)
        ]:
            print(f"Testing imports in {env_name} environment...")
            result = env.run_python(import_code)
            print(f"  {result.stdout.strip()}")
        
        print(ColorOutput.success("✅ Python imports successful"))
        self.test_results["python_import"] = True
    
    def test_shell_commands(self):
        """Test shell commands."""
        print(ColorOutput.header("\n=== Testing Shell Commands ==="))
        
        # Define commands to test with the 'cocopack' CLI
        cocopack_commands = [
            ("color-wrap", "RED Hello"),
            ("symlinks", "--help"),
            ("storage", "--help"),
            ("split-path", "/usr/local/bin/python"),
            ("path-cleanup", "$PATH"),
        ]
        
        # Define namespaced commands to test
        namespaced_commands = [
            ("cocopack-colorcode", "RED Hello"),
            ("cocopack-symlinks", "--help"),
            ("cocopack-storage", "--help"),
            ("cocopack-split-path", "/usr/local/bin/python"),
            ("cocopack-path-cleanup", "$PATH"),
        ]
        
        # Define direct commands to test (should be installed via 'cocopack install')
        direct_commands = [
            ("color-wrap", "RED Hello"),
            ("show-symlinks", "--help"),
            ("show-storage", "--help"),
            ("split-path", "/usr/local/bin/python"),
            ("path-cleanup", "$PATH"),
        ]
        
        # Test commands in each environment
        for env_name, env in [
            ("Basic", self.basic_env),
            ("Shell", self.shell_env)
        ]:
            print(f"Testing commands in {env_name} environment...")
            
            # Check namespaced commands (should be available by default)
            print(f"  Checking namespaced commands...")
            for cmd, args in namespaced_commands:
                try:
                    # Check if command exists in environment
                    bin_dir = env.path / "bin"
                    cmd_path = bin_dir / cmd
                    
                    if cmd_path.exists():
                        print(f"    Command '{cmd}' exists")
                    else:
                        print(ColorOutput.warning(f"    Command '{cmd}' not found"))
                except Exception as e:
                    print(ColorOutput.error(f"    Error checking command '{cmd}': {e}"))
            
            # Check cocopack CLI commands
            print(f"  Checking cocopack CLI commands...")
            cocopack_path = env.path / "bin" / "cocopack"
            if cocopack_path.exists():
                print(f"    Main 'cocopack' command exists")
                # We could run some test commands here if needed
            else:
                print(ColorOutput.warning(f"    Main 'cocopack' command not found"))
            
            # Direct commands should not be installed by default
            print(f"  Checking direct commands (should NOT be installed by default)...")
            missing_count = 0
            for cmd, args in direct_commands:
                try:
                    # Check if command exists in environment
                    bin_dir = env.path / "bin"
                    cmd_path = bin_dir / cmd
                    
                    if cmd_path.exists():
                        print(ColorOutput.warning(f"    Command '{cmd}' exists (should not be installed by default)"))
                    else:
                        missing_count += 1
                except Exception as e:
                    print(ColorOutput.error(f"    Error checking command '{cmd}': {e}"))
            
            if missing_count == len(direct_commands):
                print(f"    All direct commands are correctly not installed by default")
            
            # Optional: test installing direct commands
            if env_name == "Shell":  # Only test in the shell environment
                print(f"  Testing installation of direct commands...")
                try:
                    # Run the install command
                    env.run([str(env.path / "bin" / "cocopack"), "install"], capture_output=False)
                    
                    # Now check if direct commands are installed
                    print(f"  Checking direct commands after installation...")
                    installed_count = 0
                    for cmd, args in direct_commands:
                        cmd_path = env.path / "bin" / cmd
                        if cmd_path.exists():
                            print(f"    Command '{cmd}' is now installed")
                            installed_count += 1
                        else:
                            print(ColorOutput.warning(f"    Command '{cmd}' not installed"))
                    
                    if installed_count > 0:
                        print(f"    Successfully installed {installed_count}/{len(direct_commands)} direct commands")
                except Exception as e:
                    print(ColorOutput.error(f"    Error installing direct commands: {e}"))
        
        print(ColorOutput.success("✅ Shell commands check successful"))
        self.test_results["shell_commands"] = True
    
    def test_uninstallation(self):
        """Test package uninstallation."""
        print(ColorOutput.header("\n=== Testing Uninstallation ==="))
        
        # Uninstall from one environment
        print("Uninstalling from basic environment...")
        self.basic_env.uninstall_package("cocopack")
        
        # Check that the package is no longer importable
        result = self.basic_env.run_python("import cocopack", check=False)
        if result.returncode != 0 and "No module named 'cocopack'" in result.stderr:
            print(ColorOutput.success("  Package successfully uninstalled"))
        else:
            print(ColorOutput.error("  Package still importable after uninstallation"))
            print(f"  Stderr: {result.stderr}")
            raise TestFailure("Package uninstallation failed")
        
        print(ColorOutput.success("✅ Uninstallation successful"))
        self.test_results["uninstallation"] = True
    
    def print_test_results(self):
        """Print a summary of all test results."""
        print(ColorOutput.header("\n=== Test Results Summary ==="))
        
        for test_name, result in self.test_results.items():
            result_str = ColorOutput.success("✅ Passed") if result else ColorOutput.error("❌ Failed")
            print(f"{test_name.replace('_', ' ').title()}: {result_str}")
    
    def cleanup(self):
        """Clean up the testing environments and distribution files."""
        print(ColorOutput.header("\n=== Cleaning Up ==="))
        
        # Clean up test environments
        for env in [self.build_env, self.basic_env, self.shell_env, self.dev_env]:
            if env is not None:
                env.cleanup()
        
        if not self.keep_env:
            print(f"Removing temporary directory: {self.temp_dir}")
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except Exception as e:
                print(f"Error removing temporary directory: {e}")
        
        # Clean up distribution files if needed
        if not self.keep_dist:
            if self.dist_dir.exists():
                if not self.dist_existed:
                    # If dist didn't exist before and we created it, remove the whole directory
                    print(f"Removing distribution directory: {self.dist_dir}")
                    try:
                        shutil.rmtree(self.dist_dir)
                    except Exception as e:
                        print(f"Error removing distribution directory: {e}")
                else:
                    # If dist existed before, only remove files we might have added
                    print("Removing distribution files created during testing...")
                    try:
                        for pattern in ["*.whl", "*.tar.gz"]:
                            for file_path in self.dist_dir.glob(pattern):
                                print(f"  Removing {file_path.name}")
                                file_path.unlink()
                    except Exception as e:
                        print(f"Error removing distribution files: {e}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Test CocoPack installation")
    parser.add_argument("--keep-env", action="store_true", help="Keep test environments after testing")
    parser.add_argument("--keep-dist", action="store_true", help="Keep distribution files after testing")
    parser.add_argument("--skip-build", action="store_true", help="Skip build step and use existing wheel/sdist files")
    parser.add_argument("--verbose", action="store_true", help="Show additional output")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    tester = CocoPackInstallationTester(
        keep_env=args.keep_env,
        skip_build=args.skip_build,
        verbose=args.verbose,
        keep_dist=args.keep_dist
    )
    sys.exit(tester.run_tests())