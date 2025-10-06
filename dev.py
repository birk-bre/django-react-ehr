#!/usr/bin/env python3
"""
Patient EHR System - Cross-Platform Development Script
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import time
import signal
import platform
from pathlib import Path

class PatientEHRManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.is_windows = platform.system() == "Windows"
        
    def print_header(self):
        print("=" * 50)
        print("Patient EHR System - Development Manager")
        print("=" * 50)
        print()
        
    def print_menu(self):
        print("Please select an option:")
        print()
        print("1. Start Development Servers (Backend + Frontend)")
        print("2. Reset Database")
        print("3. Seed Database with Sample Data")
        print("4. Exit")
        print()
        
    def get_python_executable(self):
        """Get the correct Python executable for the virtual environment"""
        if self.is_windows:
            python_exe = Path("venv/Scripts/python.exe")
        else:
            python_exe = Path("venv/bin/python")
            
        if not python_exe.exists():
            print("Error: Virtual environment not found!")
            print("Please run 'python setup.py' first to set up the project.")
            return None
            
        return str(python_exe)
        
    def check_prerequisites(self):
        """Check if required directories and files exist"""
        errors = []
        
        # Check virtual environment
        venv_path = Path("venv")
        if not venv_path.exists():
            errors.append("Virtual environment not found! Please run 'python setup.py' first.")
            
        # Check frontend dependencies
        node_modules = Path("frontend/node_modules")
        if not node_modules.exists():
            errors.append("Frontend dependencies not installed! Please run 'python setup.py' first.")
            
        if errors:
            print("Error: Prerequisites not met!")
            for error in errors:
                print(f"  - {error}")
            return False
            
        return True
        
    def reset_database(self):
        """Reset the database to a clean state"""
        print("=" * 50)
        print("Database Reset")
        print("=" * 50)
        print()
        print("⚠️  WARNING: This will delete all data in the database!")
        print()
        
        confirmation = input("Are you sure you want to continue? (type 'yes' to confirm): ")
        if confirmation.lower() != 'yes':
            print("Reset cancelled.")
            return
            
        python_exe = self.get_python_executable()
        if not python_exe:
            return
            
        print("\nResetting database...")
        
        # Remove existing database
        db_file = Path("db.sqlite3")
        if db_file.exists():
            print("Removing old database...")
            db_file.unlink()
            print("✓ Database removed")
            
        # Run migrations
        print("Running migrations...")
        try:
            subprocess.run([python_exe, "manage.py", "migrate"], check=True)
            print("✓ Migrations completed")
        except subprocess.CalledProcessError as e:
            print(f"Error running migrations: {e}")
            return
            
        print()
        response = input("Would you like to create a new superuser? (y/n): ")
        if response.lower() in ['y', 'yes']:
            try:
                subprocess.run([python_exe, "manage.py", "createsuperuser"], check=True)
                print("✓ Superuser created")
            except subprocess.CalledProcessError:
                print("Superuser creation cancelled or failed")
                
        print()
        print("=" * 50)
        print("Database reset complete!")
        print("=" * 50)
        
    def seed_database(self):
        """Seed the database with sample data using Django management command"""
        print("=" * 50)
        print("Database Seeding")
        print("=" * 50)
        print()
        
        python_exe = self.get_python_executable()
        if not python_exe:
            return
            
        print("Would you like to:")
        print("1. Add sample data to existing database")
        print("2. Clear existing data and create fresh sample data")
        print()
        
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == "2":
            print("Creating fresh sample data (clearing existing data)...")
            try:
                subprocess.run([python_exe, "manage.py", "seed_db", "--clear"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error seeding database: {e}")
                return
        elif choice == "1":
            print("Adding sample data to existing database...")
            try:
                subprocess.run([python_exe, "manage.py", "seed_db"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error seeding database: {e}")
                return
        else:
            print("Invalid choice. Cancelled.")
            return
            
        print()
        print("=" * 50)
        print("Database seeding completed!")
        print("=" * 50)
        print()
        print("You can also run seeding manually with:")
        print(f"  {python_exe} manage.py seed_db")
        print(f"  {python_exe} manage.py seed_db --clear")
        print(f"  {python_exe} manage.py seed_db --patients 10")
                
    def start_dev_servers(self):
        """Start both backend and frontend servers"""
        print("=" * 50)
        print("Starting Development Servers")
        print("=" * 50)
        print()
        
        if not self.check_prerequisites():
            return
            
        self.setup_signal_handlers()
        
        # Start backend
        backend_started = self.start_backend()
        if not backend_started:
            print("Failed to start backend server.")
            return
            
        # Wait for backend to start
        time.sleep(3)
        
        # Start frontend
        frontend_started = self.start_frontend()
        if not frontend_started:
            print("Failed to start frontend server.")
            self.cleanup()
            return
            
        # Wait for frontend to start
        time.sleep(2)
        
        # Monitor processes
        try:
            self.monitor_processes()
        finally:
            self.cleanup()
            
    def start_backend(self):
        """Start Django backend server"""
        print("Starting Django backend...")
        
        python_exe = self.get_python_executable()
        if not python_exe:
            return False
            
        cmd = [python_exe, "manage.py", "runserver", "8000"]
        
        try:
            self.backend_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            print("✓ Backend server starting on http://localhost:8000")
            return True
        except Exception as e:
            print(f"✗ Failed to start backend: {e}")
            return False
            
    def start_frontend(self):
        """Start React frontend server"""
        print("Starting React frontend...")
        
        try:
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd="frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            print("✓ Frontend server starting on http://localhost:3000")
            return True
        except Exception as e:
            print(f"✗ Failed to start frontend: {e}")
            return False
            
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print("\n\nShutting down servers...")
            self.cleanup()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        if not self.is_windows:
            signal.signal(signal.SIGTERM, signal_handler)
            
    def cleanup(self):
        """Clean up processes"""
        if self.backend_process:
            try:
                if self.is_windows:
                    self.backend_process.terminate()
                else:
                    self.backend_process.send_signal(signal.SIGTERM)
                self.backend_process.wait(timeout=5)
            except:
                if self.backend_process.poll() is None:
                    self.backend_process.kill()
                    
        if self.frontend_process:
            try:
                if self.is_windows:
                    self.frontend_process.terminate()
                else:
                    self.frontend_process.send_signal(signal.SIGTERM)
                self.frontend_process.wait(timeout=5)
            except:
                if self.frontend_process.poll() is None:
                    self.frontend_process.kill()
                    
    def monitor_processes(self):
        """Monitor both processes and handle output"""
        print()
        print("=" * 50)
        print("Both servers are running!")
        print("Backend:  http://localhost:8000")
        print("API:      http://localhost:8000/api/")
        print("Admin:    http://localhost:8000/admin/")
        print("Frontend: http://localhost:3000")
        print()
        print("Press Ctrl+C to stop both servers")
        print("=" * 50)
        print()
        
        try:
            while True:
                backend_running = self.backend_process and self.backend_process.poll() is None
                frontend_running = self.frontend_process and self.frontend_process.poll() is None
                
                if not backend_running and not frontend_running:
                    print("Both servers have stopped.")
                    break
                elif not backend_running:
                    print("Backend server has stopped unexpectedly.")
                    break
                elif not frontend_running:
                    print("Frontend server has stopped unexpectedly.")
                    break
                    
                time.sleep(1)
                
        except KeyboardInterrupt:
            pass
            
    def run(self):
        """Main run method with menu"""
        while True:
            self.print_header()
            self.print_menu()
            
            try:
                choice = input("Enter your choice (1-4): ").strip()
                print()
                
                if choice == '1':
                    self.start_dev_servers()
                elif choice == '2':
                    self.reset_database()
                elif choice == '3':
                    self.seed_database()
                elif choice == '4':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, 3, or 4.")
                    
                if choice in ['2', '3']:
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except EOFError:
                print("\n\nGoodbye!")
                break

if __name__ == "__main__":
    manager = PatientEHRManager()
    manager.run()