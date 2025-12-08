
import shutil
import os

def copy_file(source_path, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    shutil.copy(source_path, dest_dir)
