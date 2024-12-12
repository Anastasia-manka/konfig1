import os
import datetime
from vfs import VFS

class ShellEmulator:
    def __init__(self, vfs_path, logger, username):
        self.vfs = VFS(vfs_path)
        self.logger = logger
        self.username = username
        self.cwd = "/"

    def execute(self, command):
        print(f"Processing command: {command}")  # Отладочное сообщение
        self.logger.log(self.username, command)

        parts = command.split()
        if not parts:
            return ""

        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            result = self.vfs.ls(self.cwd)
        elif cmd == "cd":
            result = self.cd(args)
        elif cmd == "rmdir":
            if len(args) != 1:
                result = "Usage: rmdir <directory>"
            else:
                result = self.vfs.rmdir(self.cwd, args[0])
        elif cmd == "date":
            result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif cmd == "tac":
            if len(args) != 1:
                result = "Usage: tac <file>"
            else:
                result = self.vfs.tac(self.cwd, args[0])
        elif cmd == "exit":
            self.logger.save()
            exit(0)
        else:
            result = f"Command not found: {cmd}"

        print(f"Result: {result}")  # Отладочное сообщение
        return result

    def cd(self, args):
        if len(args) != 1:
            return "Usage: cd <directory>"
        new_dir = args[0]
        if new_dir == "..":
            self.cwd = os.path.dirname(self.cwd)
        else:
            self.cwd = os.path.join(self.cwd, new_dir)
        return ""