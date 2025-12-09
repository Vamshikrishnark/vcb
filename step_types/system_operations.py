"""
System and Process Operations Module
Handles system commands, processes, and system checks
"""
import os
import subprocess
import psutil
import time
import shutil
from pathlib import Path


class SystemOperations:
    """Handles system and process operations for test automation"""
    
    @staticmethod
    def run_command(command, shell=True, timeout=None, working_dir=None):
        """
        Execute shell/PowerShell command
        Args:
            command: Command to execute
            shell: Run in shell context
            timeout: Command timeout in seconds
            working_dir: Working directory for command
        Returns: (success: bool, message: str, output: str)
        """
        try:
            command = command.strip()
            
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=working_dir
            )
            
            output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            
            if result.returncode == 0:
                return True, f"Command executed successfully (exit code: 0)", output
            else:
                return False, f"Command failed with exit code: {result.returncode}", output
        
        except subprocess.TimeoutExpired:
            return False, f"Command timed out after {timeout}s", ""
        except Exception as e:
            return False, f"Command execution failed: {str(e)}", ""
    
    @staticmethod
    def start_process(executable_path, arguments="", working_dir=None, wait=False, timeout=None):
        """
        Launch application/process
        Args:
            executable_path: Path to executable
            arguments: Command line arguments
            working_dir: Working directory
            wait: If True, wait for process to complete
            timeout: Timeout if wait=True
        Returns: (success: bool, message: str)
        """
        try:
            executable_path = executable_path.strip()
            
            if not os.path.exists(executable_path):
                return False, f"Executable not found: {executable_path}"
            
            command = f'"{executable_path}" {arguments}'
            
            if wait:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=working_dir,
                    timeout=timeout
                )
                return True, f"Process completed with exit code: {result.returncode}"
            else:
                subprocess.Popen(
                    command,
                    shell=True,
                    cwd=working_dir
                )
                return True, f"Process started: {executable_path}"
        
        except subprocess.TimeoutExpired:
            return False, f"Process timed out after {timeout}s"
        except Exception as e:
            return False, f"Start process failed: {str(e)}"
    
    @staticmethod
    def stop_process(process_name=None, pid=None, force=False):
        """
        Stop/kill running process
        Args:
            process_name: Name of process to stop (e.g., "notepad.exe")
            pid: Process ID to stop
            force: If True, force kill process
        Returns: (success: bool, message: str)
        """
        try:
            if not process_name and not pid:
                return False, "Either process_name or pid must be provided"
            
            stopped_count = 0
            
            if pid:
                # Stop by PID
                try:
                    process = psutil.Process(pid)
                    if force:
                        process.kill()
                    else:
                        process.terminate()
                    process.wait(timeout=5)
                    return True, f"Process stopped (PID: {pid})"
                except psutil.NoSuchProcess:
                    return False, f"Process not found (PID: {pid})"
            
            elif process_name:
                # Stop by name
                process_name = process_name.strip().lower()
                for proc in psutil.process_iter(['name', 'pid']):
                    try:
                        if proc.info['name'].lower() == process_name:
                            if force:
                                proc.kill()
                            else:
                                proc.terminate()
                            stopped_count += 1
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                if stopped_count > 0:
                    return True, f"Stopped {stopped_count} process(es) named '{process_name}'"
                else:
                    return False, f"No running process found with name '{process_name}'"
        
        except Exception as e:
            return False, f"Stop process failed: {str(e)}"
    
    @staticmethod
    def check_process_running(process_name=None, pid=None, should_run=True):
        """
        Check if process is running
        Args:
            process_name: Name of process to check
            pid: Process ID to check
            should_run: If True, pass when running; if False, pass when not running
        Returns: (success: bool, message: str)
        """
        try:
            if not process_name and not pid:
                return False, "Either process_name or pid must be provided"
            
            is_running = False
            found_pids = []
            
            if pid:
                # Check by PID
                is_running = psutil.pid_exists(pid)
                if is_running:
                    found_pids.append(pid)
            
            elif process_name:
                # Check by name
                process_name = process_name.strip().lower()
                for proc in psutil.process_iter(['name', 'pid']):
                    try:
                        if proc.info['name'].lower() == process_name:
                            is_running = True
                            found_pids.append(proc.info['pid'])
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            
            if should_run:
                if is_running:
                    return True, f"Process is running (PIDs: {found_pids})"
                else:
                    return False, f"Process is not running"
            else:
                if not is_running:
                    return True, f"Process is not running (as expected)"
                else:
                    return False, f"Process is still running (PIDs: {found_pids})"
        
        except Exception as e:
            return False, f"Check process failed: {str(e)}"
    
    @staticmethod
    def check_disk_space(path, required_gb=None, required_percent=None):
        """
        Check available disk space
        Args:
            path: Path to check (drive or directory)
            required_gb: Minimum required space in GB
            required_percent: Minimum required free space percentage
        Returns: (success: bool, message: str)
        """
        try:
            path = path.strip()
            
            if not os.path.exists(path):
                return False, f"Path does not exist: {path}"
            
            usage = shutil.disk_usage(path)
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            free_gb = usage.free / (1024**3)
            free_percent = (usage.free / usage.total) * 100
            
            info = f"Disk: {total_gb:.2f}GB total, {used_gb:.2f}GB used, {free_gb:.2f}GB free ({free_percent:.1f}%)"
            
            if required_gb:
                if free_gb >= required_gb:
                    return True, f"✓ Sufficient space: {free_gb:.2f}GB available (required: {required_gb}GB). {info}"
                else:
                    return False, f"✗ Insufficient space: {free_gb:.2f}GB available (required: {required_gb}GB). {info}"
            
            elif required_percent:
                if free_percent >= required_percent:
                    return True, f"✓ Sufficient space: {free_percent:.1f}% free (required: {required_percent}%). {info}"
                else:
                    return False, f"✗ Insufficient space: {free_percent:.1f}% free (required: {required_percent}%). {info}"
            
            else:
                return True, info
        
        except Exception as e:
            return False, f"Check disk space failed: {str(e)}"
    
    @staticmethod
    def check_memory(required_mb=None, required_percent=None):
        """
        Check available system memory
        Args:
            required_mb: Minimum required memory in MB
            required_percent: Minimum required free memory percentage
        Returns: (success: bool, message: str)
        """
        try:
            memory = psutil.virtual_memory()
            total_mb = memory.total / (1024**2)
            available_mb = memory.available / (1024**2)
            used_mb = memory.used / (1024**2)
            percent_used = memory.percent
            percent_available = 100 - percent_used
            
            info = f"Memory: {total_mb:.0f}MB total, {used_mb:.0f}MB used, {available_mb:.0f}MB available ({percent_available:.1f}% free)"
            
            if required_mb:
                if available_mb >= required_mb:
                    return True, f"✓ Sufficient memory: {available_mb:.0f}MB available (required: {required_mb}MB). {info}"
                else:
                    return False, f"✗ Insufficient memory: {available_mb:.0f}MB available (required: {required_mb}MB). {info}"
            
            elif required_percent:
                if percent_available >= required_percent:
                    return True, f"✓ Sufficient memory: {percent_available:.1f}% free (required: {required_percent}%). {info}"
                else:
                    return False, f"✗ Insufficient memory: {percent_available:.1f}% free (required: {required_percent}%). {info}"
            
            else:
                return True, info
        
        except Exception as e:
            return False, f"Check memory failed: {str(e)}"
    
    @staticmethod
    def get_system_info():
        """
        Get comprehensive system information
        Returns: (success: bool, message: str)
        """
        try:
            info = []
            
            # CPU info
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_percent = psutil.cpu_percent(interval=1)
            info.append(f"CPU: {cpu_count} cores ({cpu_count_logical} logical), {cpu_percent}% used")
            
            # Memory info
            memory = psutil.virtual_memory()
            info.append(f"Memory: {memory.total/(1024**3):.1f}GB total, {memory.percent}% used")
            
            # Disk info
            disk = shutil.disk_usage('/')
            info.append(f"Disk: {disk.total/(1024**3):.1f}GB total, {disk.free/(1024**3):.1f}GB free")
            
            # OS info
            import platform
            info.append(f"OS: {platform.system()} {platform.release()} ({platform.machine()})")
            
            return True, "\n".join(info)
        
        except Exception as e:
            return False, f"Get system info failed: {str(e)}"
