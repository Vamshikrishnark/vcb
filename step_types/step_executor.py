"""
Step Executor Module
Executes different step types and returns results
"""
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from step_types.file_operations import FileOperations
from step_types.system_operations import SystemOperations


class StepExecutor:
    """Executes test steps and returns results"""
    
    @staticmethod
    def execute_step(step_type, details):
        """
        Execute a test step based on its type
        Args:
            step_type: Type of step to execute
            details: Dictionary of step details/parameters
        Returns:
            (success: bool, message: str, output: str)
        """
        try:
            # File Operations
            if step_type == "Move File":
                success, msg = FileOperations.move_file(
                    details.get("from_path", ""),
                    details.get("to_path", "")
                )
                return success, msg, msg
            
            elif step_type == "Delete File/Folder":
                recursive = details.get("recursive_var", False)
                if hasattr(recursive, 'get'):
                    recursive = recursive.get()
                success, msg = FileOperations.delete_path(
                    details.get("path", ""),
                    recursive=recursive
                )
                return success, msg, msg
            
            elif step_type == "Rename File":
                success, msg = FileOperations.rename_path(
                    details.get("old_path", ""),
                    details.get("new_path", "")
                )
                return success, msg, msg
            
            elif step_type == "Create Directory":
                create_parents = details.get("create_parents_var", True)
                if hasattr(create_parents, 'get'):
                    create_parents = create_parents.get()
                success, msg = FileOperations.create_directory(
                    details.get("path", ""),
                    create_parents=create_parents
                )
                return success, msg, msg
            
            elif step_type == "Check File Exists":
                should_exist = details.get("should_exist", "Yes") == "Yes"
                success, msg = FileOperations.check_path_exists(
                    details.get("path", ""),
                    should_exist=should_exist
                )
                return success, msg, msg
            
            elif step_type == "Compare Files":
                success, msg = FileOperations.compare_files(
                    details.get("file1", ""),
                    details.get("file2", ""),
                    method=details.get("method", "checksum")
                )
                return success, msg, msg
            
            elif step_type == "Extract Archive":
                success, msg = FileOperations.extract_archive(
                    details.get("archive_path", ""),
                    details.get("extract_to", ""),
                    archive_type=details.get("archive_type", "auto")
                )
                return success, msg, msg
            
            elif step_type == "Wait for File":
                should_exist = details.get("should_exist", "File to Appear") == "File to Appear"
                timeout = int(details.get("timeout", 60))
                success, msg = FileOperations.wait_for_file(
                    details.get("file_path", ""),
                    timeout=timeout,
                    should_exist=should_exist
                )
                return success, msg, msg
            
            # System Operations
            elif step_type == "Run Command":
                command = details.get("command", "")
                if hasattr(command, 'get'):
                    command = command.get("1.0", "end-1c")
                
                timeout = details.get("timeout", "30")
                try:
                    timeout = int(timeout) if timeout else None
                except:
                    timeout = None
                
                working_dir = details.get("working_dir", "") or None
                
                success, msg, output = SystemOperations.run_command(
                    command,
                    timeout=timeout,
                    working_dir=working_dir
                )
                return success, msg, output
            
            elif step_type == "Start Process":
                wait = details.get("wait_var", False)
                if hasattr(wait, 'get'):
                    wait = wait.get()
                
                success, msg = SystemOperations.start_process(
                    details.get("executable", ""),
                    arguments=details.get("arguments", ""),
                    wait=wait
                )
                return success, msg, msg
            
            elif step_type == "Stop Process":
                force = details.get("force_var", False)
                if hasattr(force, 'get'):
                    force = force.get()
                
                pid = details.get("pid", "")
                pid = int(pid) if pid else None
                
                process_name = details.get("process_name", "") or None
                
                success, msg = SystemOperations.stop_process(
                    process_name=process_name,
                    pid=pid,
                    force=force
                )
                return success, msg, msg
            
            elif step_type == "Check Process Running":
                should_run = details.get("should_run", "Yes") == "Yes"
                success, msg = SystemOperations.check_process_running(
                    process_name=details.get("process_name", ""),
                    should_run=should_run
                )
                return success, msg, msg
            
            elif step_type == "Check Disk Space":
                required_gb = details.get("required_gb", "")
                try:
                    required_gb = float(required_gb) if required_gb else None
                except:
                    required_gb = None
                
                success, msg = SystemOperations.check_disk_space(
                    details.get("path", "C:/"),
                    required_gb=required_gb
                )
                return success, msg, msg
            
            elif step_type == "Check Memory":
                required_mb = details.get("required_mb", "")
                try:
                    required_mb = float(required_mb) if required_mb else None
                except:
                    required_mb = None
                
                success, msg = SystemOperations.check_memory(
                    required_mb=required_mb
                )
                return success, msg, msg
            
            else:
                return False, f"Unknown step type: {step_type}", ""
        
        except Exception as e:
            return False, f"Step execution error: {str(e)}", str(e)
