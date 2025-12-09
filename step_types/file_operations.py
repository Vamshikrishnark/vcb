"""
File and Directory Operations Module
Handles all file/folder related test operations
"""
import os
import shutil
import hashlib
import zipfile
import tarfile
import time
from pathlib import Path


class FileOperations:
    """Handles file and directory operations for test automation"""
    
    @staticmethod
    def move_file(source_path, destination_path):
        """
        Move file(s) from source to destination
        Returns: (success: bool, message: str)
        """
        try:
            source_path = source_path.strip()
            destination_path = destination_path.strip()
            
            if not os.path.exists(source_path):
                return False, f"Source does not exist: {source_path}"
            
            # Ensure destination directory exists
            dest_dir = os.path.dirname(destination_path) if os.path.isfile(source_path) else destination_path
            os.makedirs(dest_dir, exist_ok=True)
            
            # Move the file/directory
            shutil.move(source_path, destination_path)
            return True, f"Successfully moved {source_path} to {destination_path}"
        except Exception as e:
            return False, f"Move failed: {str(e)}"
    
    @staticmethod
    def delete_path(path, recursive=False):
        """
        Delete file or directory
        Args:
            path: Path to delete
            recursive: If True, delete directories recursively
        Returns: (success: bool, message: str)
        """
        try:
            path = path.strip()
            
            if not os.path.exists(path):
                return False, f"Path does not exist: {path}"
            
            if os.path.isfile(path):
                os.remove(path)
                return True, f"Successfully deleted file: {path}"
            elif os.path.isdir(path):
                if recursive:
                    shutil.rmtree(path)
                    return True, f"Successfully deleted directory: {path}"
                else:
                    os.rmdir(path)
                    return True, f"Successfully deleted empty directory: {path}"
        except Exception as e:
            return False, f"Delete failed: {str(e)}"
    
    @staticmethod
    def rename_path(old_path, new_path):
        """
        Rename file or directory
        Returns: (success: bool, message: str)
        """
        try:
            old_path = old_path.strip()
            new_path = new_path.strip()
            
            if not os.path.exists(old_path):
                return False, f"Source does not exist: {old_path}"
            
            if os.path.exists(new_path):
                return False, f"Destination already exists: {new_path}"
            
            os.rename(old_path, new_path)
            return True, f"Successfully renamed {old_path} to {new_path}"
        except Exception as e:
            return False, f"Rename failed: {str(e)}"
    
    @staticmethod
    def create_directory(path, create_parents=True):
        """
        Create directory
        Args:
            path: Directory path to create
            create_parents: If True, create parent directories if needed
        Returns: (success: bool, message: str)
        """
        try:
            path = path.strip()
            
            if os.path.exists(path):
                return True, f"Directory already exists: {path}"
            
            if create_parents:
                os.makedirs(path, exist_ok=True)
            else:
                os.mkdir(path)
            
            return True, f"Successfully created directory: {path}"
        except Exception as e:
            return False, f"Create directory failed: {str(e)}"
    
    @staticmethod
    def check_path_exists(path, should_exist=True):
        """
        Check if file or directory exists
        Args:
            path: Path to check
            should_exist: If True, pass when exists; if False, pass when doesn't exist
        Returns: (success: bool, message: str)
        """
        try:
            path = path.strip()
            exists = os.path.exists(path)
            
            if should_exist:
                if exists:
                    path_type = "directory" if os.path.isdir(path) else "file"
                    return True, f"Path exists ({path_type}): {path}"
                else:
                    return False, f"Path does not exist: {path}"
            else:
                if not exists:
                    return True, f"Path does not exist (as expected): {path}"
                else:
                    return False, f"Path exists (unexpected): {path}"
        except Exception as e:
            return False, f"Check path failed: {str(e)}"
    
    @staticmethod
    def compare_files(file1_path, file2_path, method="checksum"):
        """
        Compare two files
        Args:
            file1_path: First file path
            file2_path: Second file path
            method: Comparison method - "checksum", "content", "size"
        Returns: (success: bool, message: str)
        """
        try:
            file1_path = file1_path.strip()
            file2_path = file2_path.strip()
            
            if not os.path.isfile(file1_path):
                return False, f"First file does not exist: {file1_path}"
            
            if not os.path.isfile(file2_path):
                return False, f"Second file does not exist: {file2_path}"
            
            if method == "size":
                size1 = os.path.getsize(file1_path)
                size2 = os.path.getsize(file2_path)
                if size1 == size2:
                    return True, f"Files have same size: {size1} bytes"
                else:
                    return False, f"Files have different sizes: {size1} vs {size2} bytes"
            
            elif method == "checksum":
                hash1 = FileOperations._calculate_checksum(file1_path)
                hash2 = FileOperations._calculate_checksum(file2_path)
                if hash1 == hash2:
                    return True, f"Files are identical (MD5: {hash1})"
                else:
                    return False, f"Files are different (MD5: {hash1} vs {hash2})"
            
            elif method == "content":
                with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
                    content1 = f1.read()
                    content2 = f2.read()
                    if content1 == content2:
                        return True, f"Files have identical content ({len(content1)} bytes)"
                    else:
                        return False, f"Files have different content"
            
            else:
                return False, f"Unknown comparison method: {method}"
        
        except Exception as e:
            return False, f"File comparison failed: {str(e)}"
    
    @staticmethod
    def _calculate_checksum(file_path, algorithm="md5"):
        """Calculate file checksum"""
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    @staticmethod
    def extract_archive(archive_path, extract_to, archive_type="auto"):
        """
        Extract compressed archive
        Args:
            archive_path: Path to archive file
            extract_to: Destination directory
            archive_type: "auto", "zip", "tar", "tar.gz"
        Returns: (success: bool, message: str)
        """
        try:
            archive_path = archive_path.strip()
            extract_to = extract_to.strip()
            
            if not os.path.isfile(archive_path):
                return False, f"Archive does not exist: {archive_path}"
            
            # Create extraction directory
            os.makedirs(extract_to, exist_ok=True)
            
            # Auto-detect archive type
            if archive_type == "auto":
                if archive_path.endswith('.zip'):
                    archive_type = "zip"
                elif archive_path.endswith(('.tar.gz', '.tgz')):
                    archive_type = "tar.gz"
                elif archive_path.endswith('.tar'):
                    archive_type = "tar"
                else:
                    return False, f"Unknown archive type for: {archive_path}"
            
            # Extract based on type
            if archive_type == "zip":
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
                return True, f"Successfully extracted ZIP archive to: {extract_to}"
            
            elif archive_type in ["tar", "tar.gz"]:
                mode = "r:gz" if archive_type == "tar.gz" else "r"
                with tarfile.open(archive_path, mode) as tar_ref:
                    tar_ref.extractall(extract_to)
                return True, f"Successfully extracted TAR archive to: {extract_to}"
            
            else:
                return False, f"Unsupported archive type: {archive_type}"
        
        except Exception as e:
            return False, f"Extract archive failed: {str(e)}"
    
    @staticmethod
    def wait_for_file(file_path, timeout=60, should_exist=True, check_interval=1):
        """
        Wait for file to appear or disappear
        Args:
            file_path: Path to monitor
            timeout: Maximum wait time in seconds
            should_exist: If True, wait for file to appear; if False, wait for it to disappear
            check_interval: Time between checks in seconds
        Returns: (success: bool, message: str)
        """
        try:
            file_path = file_path.strip()
            start_time = time.time()
            
            while (time.time() - start_time) < timeout:
                exists = os.path.exists(file_path)
                
                if should_exist and exists:
                    elapsed = time.time() - start_time
                    return True, f"File appeared after {elapsed:.2f}s: {file_path}"
                elif not should_exist and not exists:
                    elapsed = time.time() - start_time
                    return True, f"File disappeared after {elapsed:.2f}s: {file_path}"
                
                time.sleep(check_interval)
            
            # Timeout reached
            if should_exist:
                return False, f"Timeout: File did not appear within {timeout}s: {file_path}"
            else:
                return False, f"Timeout: File did not disappear within {timeout}s: {file_path}"
        
        except Exception as e:
            return False, f"Wait for file failed: {str(e)}"
