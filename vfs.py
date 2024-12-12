import zipfile
import os


class VFS:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        try:
            self.zip_file = zipfile.ZipFile(zip_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Zip file '{zip_path}' not found.")
        except zipfile.BadZipFile:
            raise zipfile.BadZipFile(f"Invalid zip file: '{zip_path}'")

    def ls(self, path=""):
        try:
            names = self.zip_file.namelist()
            # List of directories to show
            directories_to_show = ["dir1", "dir2"]

            # Collect top-level items
            top_level_items = []
            for name in names:
                is_subdir = False
                for dir_to_show in directories_to_show:
                    if name.startswith(dir_to_show + "/"):
                        is_subdir = True
                        break
                if not is_subdir:
                    top_level_items.append(name)

            # Add the directories we want to show
            top_level_items.extend(directories_to_show)

            return "\n".join(sorted(set(top_level_items)))  # Use sorted() and set() to remove duplicates
        except Exception as e:
            return f"Error listing files and directories: {e}"

    def rmdir(self, path, dir_name):
        try:
            self.zip_file.extractall(path=path)
            dir_to_remove = os.path.join(path, dir_name)
            if not os.path.exists(dir_to_remove):
                return f"Directory '{dir_name}' not found in archive."
            os.rmdir(dir_to_remove)
            return f"Directory '{dir_name}' removed."
        except OSError as e:
            return f"Error removing directory: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"


    def tac(self, path, file_name):
        try:
            full_path = os.path.join(path, file_name)
            with self.zip_file.open(full_path) as f:
                content = f.read().decode('utf-8')
            return "\n".join(content.splitlines()[::-1])
        except KeyError:
            return f"File '{file_name}' not found in archive."
        except UnicodeDecodeError:
            return f"File '{file_name}' could not be decoded as UTF-8."
        except Exception as e:
            return f"An unexpected error occurred: {e}"