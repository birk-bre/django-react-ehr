#!/usr/bin/env python3
"""
Patient EHR System - Cross-Platform Setup Script
Sets up the complete development environment
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class ProjectSetup:
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.python_cmd = self.get_python_command()
        
    def get_python_command(self):
        """Get the appropriate Python command for this system"""
        # Try different Python commands
        for cmd in ['python3', 'python']:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, check=True)
                if 'Python 3.' in result.stdout:
                    return cmd
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        return None
        
    def print_header(self):
        print("=" * 50)
        print("Patient EHR System - Initial Setup")
        print("=" * 50)
        print()
        
    def print_colored(self, text, color=''):
        """Print colored text (simplified for cross-platform)"""
        colors = {
            'red': '\033[0;31m',
            'green': '\033[0;32m',
            'yellow': '\033[1;33m',
            'reset': '\033[0m'
        }
        
        if color in colors and not self.is_windows:
            print(f"{colors[color]}{text}{colors['reset']}")
        else:
            print(text)
            
    def check_python(self):
        """Check Python installation"""
        print("Checking Python installation...")
        
        if not self.python_cmd:
            self.print_colored("Error: Python 3 is not installed or not found in PATH", 'red')
            print("Please install Python 3.11+ from https://python.org/")
            return False
            
        try:
            result = subprocess.run([self.python_cmd, '--version'], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            self.print_colored(f"✓ {version} found", 'green')
            return True
        except subprocess.CalledProcessError:
            self.print_colored("Error: Could not get Python version", 'red')
            return False
            
    def check_node(self):
        """Check Node.js installation"""
        print("Checking Node.js installation...")
        
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            self.print_colored(f"✓ Node.js {version} found", 'green')
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_colored("Error: Node.js is not installed", 'red')
            print("Please install Node.js 18+ from https://nodejs.org/")
            return False
            
    def setup_backend(self):
        """Setup Django backend"""
        print("=" * 50)
        print("Setting up Backend (Django)")
        print("=" * 50)
        print()
        
        # Check if virtual environment exists
        venv_path = Path("venv")
        if venv_path.exists():
            self.print_colored("Virtual environment already exists", 'yellow')
        else:
            print("Creating Python virtual environment...")
            try:
                subprocess.run([self.python_cmd, '-m', 'venv', 'venv'], check=True)
                self.print_colored("✓ Virtual environment created", 'green')
            except subprocess.CalledProcessError as e:
                self.print_colored(f"Error creating virtual environment: {e}", 'red')
                return False
                
        # Get virtual environment Python executable
        if self.is_windows:
            venv_python = Path("venv/Scripts/python.exe")
            venv_pip = Path("venv/Scripts/pip.exe")
        else:
            venv_python = Path("venv/bin/python")
            venv_pip = Path("venv/bin/pip")
            
        if not venv_python.exists():
            self.print_colored("Error: Virtual environment Python not found", 'red')
            return False
            
        print("Activating virtual environment...")
        self.print_colored("✓ Virtual environment activated", 'green')
        print()
        
        # Upgrade pip
        print("Upgrading pip...")
        try:
            subprocess.run([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'], 
                         check=True, capture_output=True)
            self.print_colored("✓ pip upgraded", 'green')
        except subprocess.CalledProcessError as e:
            self.print_colored(f"Warning: Could not upgrade pip: {e}", 'yellow')
        print()
        
        # Install Python dependencies
        print("Installing Python dependencies...")
        dependencies = [
            'django',
            'djangorestframework', 
            'django-cors-headers',
        ]
        
        # Check if requirements.txt exists and use it
        if Path("requirements.txt").exists():
            print("Found requirements.txt, installing from file...")
            try:
                subprocess.run([str(venv_python), '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                             check=True)
                self.print_colored("✓ Python dependencies installed from requirements.txt", 'green')
            except subprocess.CalledProcessError as e:
                self.print_colored(f"Error installing from requirements.txt: {e}", 'red')
                print("Falling back to individual package installation...")
                try:
                    for dep in dependencies:
                        subprocess.run([str(venv_python), '-m', 'pip', 'install', dep], check=True)
                    self.print_colored("✓ Python dependencies installed", 'green')
                except subprocess.CalledProcessError as e:
                    self.print_colored(f"Error installing dependencies: {e}", 'red')
                    return False
        else:
            try:
                for dep in dependencies:
                    print(f"Installing {dep}...")
                    subprocess.run([str(venv_python), '-m', 'pip', 'install', dep], check=True)
                self.print_colored("✓ Python dependencies installed", 'green')
            except subprocess.CalledProcessError as e:
                self.print_colored(f"Error installing dependencies: {e}", 'red')
                return False
        print()
        
        # Run migrations
        print("Running database migrations...")
        try:
            subprocess.run([str(venv_python), 'manage.py', 'migrate'], check=True)
            self.print_colored("✓ Database migrations completed", 'green')
        except subprocess.CalledProcessError as e:
            self.print_colored(f"Error running migrations: {e}", 'red')
            return False
        print()
        
        # Ask to create superuser
        try:
            print("Would you like to create a Django superuser now? ")
            print("This will allow you to access the admin interface.")
            print("You can create one later with: python manage.py createsuperuser")
            response = input("(y/n): ").strip().lower()
            if response in ['y', 'yes']:
                print("Creating superuser...")
                subprocess.run([str(venv_python), 'manage.py', 'createsuperuser'])
                self.print_colored("✓ Superuser created", 'green')
            else:
                print("Skipping superuser creation")
                print("You can create one later with: python manage.py createsuperuser")
        except KeyboardInterrupt:
            print("\nSkipping superuser creation")
        print()
        
        return True
        
    def setup_frontend(self):
        """Setup React frontend"""
        print("=" * 50)
        print("Setting up Frontend (React)")
        print("=" * 50)
        print()
        
        frontend_path = Path("frontend")
        if not frontend_path.exists():
            self.print_colored("Error: frontend directory not found", 'red')
            return False
            
        os.chdir(frontend_path)
        
        # Install frontend dependencies
        print("Installing frontend dependencies...")
        try:
            # Check if package-lock.json exists, use npm ci if it does
            if Path("package-lock.json").exists():
                subprocess.run(['npm', 'ci'], check=True)
            else:
                subprocess.run(['npm', 'install'], check=True)
            self.print_colored("✓ Frontend dependencies installed", 'green')
        except subprocess.CalledProcessError as e:
            self.print_colored(f"Error installing frontend dependencies: {e}", 'red')
            return False
        finally:
            os.chdir('..')
            
        print()
        return True
    
                
    def print_completion_message(self):
        """Print setup completion message"""
        print("=" * 50)
        print("Setup Complete!")
        print("=" * 50)
        print()
        print("Next steps:")
        print()
        
        if self.is_windows:
            self.print_colored("1. Start the development manager:", 'green')
            print("   python dev.py")
            print("   (or double-click start.bat)")
        else:
            self.print_colored("1. Start the development manager:", 'green')
            print("   python dev.py")
            print("   (or ./dev.py)")
            
        print()
        print("2. From the menu you can:")
        print("   - Start both development servers")
        print("   - Reset the database")
        print("   - Seed the database with sample data")
        print()
        print("3. Access the application once servers are running:")
        self.print_colored("   Frontend: http://localhost:3000", 'green')
        self.print_colored("   Backend:  http://localhost:8000/api/", 'green')
        self.print_colored("   Admin:    http://localhost:8000/admin/", 'green')
        print()
        
        if not self.is_windows:
            self.print_colored("Note: Remember to activate the virtual environment when running Django commands manually:", 'yellow')
            print("   source venv/bin/activate")
        else:
            self.print_colored("Note: Remember to activate the virtual environment when running Django commands manually:", 'yellow')
            print("   venv\\Scripts\\activate")
        print()
        
    def run(self):
        """Main setup process"""
        self.print_header()
        
        # Check prerequisites
        if not self.check_python():
            return False
        print()
        
        if not self.check_node():
            return False
        print()
        
        # Setup backend
        if not self.setup_backend():
            return False
            
        # Setup frontend
        if not self.setup_frontend():
            return False
        # Print completion message
        self.print_completion_message()
        
        return True

if __name__ == "__main__":
    setup = ProjectSetup()
    success = setup.run()
    
    if not success:
        print()
        print("Setup failed. Please check the errors above and try again.")
        sys.exit(1)
    else:
        sys.exit(0)