import os
import shutil
import tarfile
import zipfile
from datetime import datetime, timedelta

def back_up_dir(dir_path: str, dest_path: str):
    """Back up files from the source directory to the destination directory."""
    if not os.path.exists(dir_path):
        print(f"Error: Source directory '{dir_path}' does not exist.")
        return
    if not os.path.exists(dest_path):
        print(f"Error: Destination directory '{dest_path}' does not exist.")
        return

    try:
        shutil.copytree(dir_path, dest_path, dirs_exist_ok=True)
        print(f"Backup completed successfully from '{dir_path}' to '{dest_path}'.")
    except Exception as e:
        print(f"Error during backup: {e}")

def archive_dir(dir_name: str, arch_type: str, archive_base_name: str):
    """Create an archive of the specified directory."""
    valid_types = {"zip", "gztar", "tar", "bztar", "xztar"}
    if not os.path.exists(dir_name):
        print(f"Error: Directory '{dir_name}' does not exist.")
        return
    if arch_type not in valid_types:
        print(f"Error: Invalid archive type '{arch_type}'. Valid types are: {', '.join(valid_types)}.")
        return

    archive_path = os.path.join(os.path.expanduser("~"), archive_base_name)
    try:
        shutil.make_archive(archive_path, arch_type, dir_name)
        print(f"Archive created successfully at '{archive_path}.{arch_type}'.")
    except Exception as e:
        print(f"Error during archiving: {e}")

def get_large_archive(zip_file_path: str, threshold: int):
    """List files larger than the threshold in a zip archive and show the OS that created it."""
    if not os.path.isfile(zip_file_path):
        print(f"Error: File '{zip_file_path}' does not exist.")
        return

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zf:
            print(f"Archive created by: {zf.comment.decode('utf-8') if zf.comment else 'Unknown OS'}")
            for info in zf.infolist():
                if info.file_size > threshold * 1024:
                    print(f"{info.filename}: {info.file_size / 1024:.2f} KB")
    except Exception as e:
        print(f"Error processing zip file: {e}")

def display_recent_files(dir_path=None):
    """Display files modified in the last month."""
    dir_path = dir_path or os.getcwd()
    if not os.path.exists(dir_path):
        print(f"Error: Directory '{dir_path}' does not exist.")
        return

    try:
        cutoff_date = datetime.now() - timedelta(days=30)
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime > cutoff_date:
                    print(f"{file_path} - Last modified: {mtime}")
    except Exception as e:
        print(f"Error displaying recent files: {e}")

def menu():
    """Display a menu system for selecting functionality."""
    while True:
        print("\nMenu:")
        print("1. Backup Directory")
        print("2. Archive Directory")
        print("3. Get Large Files in Archive")
        print("4. Display Recent Files")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            src = input("Enter the source directory: ")
            dest = input("Enter the destination directory: ")
            back_up_dir(src, dest)
        elif choice == "2":
            dir_name = input("Enter the directory to archive: ")
            arch_type = input("Enter the archive type (zip, gztar, tar, bztar, xztar): ")
            base_name = input("Enter the base name for the archive: ")
            archive_dir(dir_name, arch_type, base_name)
        elif choice == "3":
            zip_path = input("Enter the zip file path: ")
            threshold = int(input("Enter the size threshold in KB: "))
            get_large_archive(zip_path, threshold)
        elif choice == "4":
            dir_path = input("Enter the directory (leave blank for current): ")
            display_recent_files(dir_path.strip() or None)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
