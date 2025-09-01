#!/usr/bin/env python3
"""
Test PyPI build workflow locally to verify package structure before publishing.
This script:
1. Creates a temporary build environment
2. Builds the package using the same commands as the GitHub workflow
3. Installs the built package in a temporary environment
4. Runs basic import tests to ensure the package is installable and importable
"""

import os, sys
import venv
import shutil
import tempfile
import subprocess
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return its output."""
    print(f"\n=== Running: {cmd} ===")
    result = subprocess.run(
        cmd, 
        shell=True, 
        cwd=cwd, 
        text=True, 
        capture_output=True
    )
    
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}", file=sys.stderr)
        return False
    return True


def create_venv(venv_path):
    """Create a virtual environment."""
    print(f"\n=== Creating virtual environment at {venv_path} ===")
    venv.create(venv_path, with_pip=True)
    
    # Get the path to the python executable in the venv
    if sys.platform == 'win32':
        python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        python_exe = os.path.join(venv_path, 'bin', 'python')
    
    return python_exe


def main():
    # Get the repository root directory
    repo_root = Path(__file__).parent.parent.absolute()
    
    # Create a temporary directory for our test
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        print(f"Using temporary directory: {temp_dir_path}")
        
        # Create directories for different stages
        build_dir = temp_dir_path / "build"
        install_dir = temp_dir_path / "install"
        dist_dir = repo_root / "dist"
        
        # Create directories
        build_dir.mkdir()
        install_dir.mkdir()
        
        # Clean any existing dist directory
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        
        # Create virtual environments
        build_python = create_venv(build_dir)
        install_python = create_venv(install_dir)
        
        # Install build dependencies
        if not run_command(f"{build_python} -m pip install --upgrade pip build", cwd=repo_root):
            return 1
        
        # Build the package - this simulates what happens in the GitHub workflow
        if not run_command(f"{build_python} -m build", cwd=repo_root):
            print("Package build failed!")
            return 1
        
        # Check that the dist directory now contains wheel and sdist files
        if not dist_dir.exists() or not list(dist_dir.glob("*.whl")) or not list(dist_dir.glob("*.tar.gz")):
            print("Build did not produce expected files in dist/")
            return 1
        
        print("\n=== Build successful! ===")
        
        # Install the built package in the test environment
        wheel_file = list(dist_dir.glob("*.whl"))[0]
        if not run_command(f"{install_python} -m pip install {wheel_file}", cwd=repo_root):
            print("Package installation failed!")
            return 1
        
        # Write a simple test script to verify imports work
        test_script = install_dir / "test_import.py"
        with open(test_script, "w") as f:
            f.write("""
import sys
print(f"Python version: {sys.version}")
print("Attempting to import cocopack...")
import cocopack
print(f"Successfully imported cocopack (version {cocopack.__version__})")
try:
    import cocopack.notebook
    print("Successfully imported cocopack.notebook")
except ImportError as e:
    print(f"Error importing cocopack.notebook: {e}")
    sys.exit(1)
try:
    import cocopack.shellpack
    print("Successfully imported cocopack.shellpack")
except ImportError as e:
    print(f"Error importing cocopack.shellpack: {e}")
    sys.exit(1)
print("All imports successful!")
""")
        
        # Run the test script
        if not run_command(f"{install_python} {test_script}"):
            print("Package import test failed!")
            return 1
        
        print("\n=== All tests passed! ===")
        print("The package builds successfully and can be imported correctly.")
        print(f"Built files available in {dist_dir}")
        
        return 0


if __name__ == "__main__":
    sys.exit(main())