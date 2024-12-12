import tkinter as tk
from tkinter import scrolledtext
import toml
from shell_emulator import ShellEmulator
from logger import Logger

class ShellGUI:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.logger = Logger(config['log_path'])
        self.shell = ShellEmulator(config['vfs_path'], self.logger, config['username'])

        self.text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text.pack()

        self.prompt()

    def prompt(self):
        prompt_text = f"{self.shell.username}@{self.shell.cwd} $ "
        self.text.insert(tk.END, prompt_text)
        self.text.insert(tk.END, "\n")  # Добавляем перевод строки
        # Важно: Сдвигаем курсор на 0 позицию.
        self.text.mark_set("insert", tk.END)
        self.text.see(tk.END)
        self.text.bind("<Return>", self.handle_command)

    def handle_command(self, event):
        cursor_position = self.text.index("insert")
        prompt_line_start = self.text.search(
            f"{self.shell.username}@{self.shell.cwd} $ ", cursor_position + "-1c", "1.0", backwards=True
        )

        if not prompt_line_start:
            self.prompt()
            return

        command_start = f"{prompt_line_start}+{len(f'{self.shell.username}@{self.shell.cwd} $ ')}c"
        command = self.text.get(command_start, "insert").strip()

        if not command:
            return

        self.text.mark_set("insert", command_start)  # Устанавливаем курсор

        try:
            output = self.shell.execute(command)
        except Exception as e:
            output = f"Ошибка: {e}"

        if output:
            self.text.insert(tk.END, output)
        else:
            self.text.delete(command_start, tk.END)  # Очищаем строку в случае пустого вывода

        self.text.insert(tk.END, "\n")
        self.prompt()


def main():
    with open("config.toml", "r") as f:
        try:
            config = toml.load(f)
        except toml.TomlDecodeError as e:
            print(f"Ошибка cnncnc при чтении config.toml: {e}")
            return

    root = tk.Tk()
    root.title("Anastasiia Karpova")  # Изменяем заголовок окна
    try:
        ShellGUI(root, config)
    except Exception as e:
        print(f"Ошибка при инициализации ShellGUI: {e}")
        return
    root.mainloop()


if __name__ == "__main__":
    main()