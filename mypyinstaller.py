import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import re

def update_pyinstaller_command_display():
    command = construct_pyinstaller_command()
    command_display.set(' '.join(command))

def construct_pyinstaller_command():
    command = ["pyinstaller"]
    
    if onefile_var.get():
        command.append("--onefile")
    
    if windowed_var.get():
        command.append("--windowed")
    
    for hidden_import in hidden_imports:
        command.extend(["--hidden-import", hidden_import])
    
    for source, dest in add_data.items():
        command.extend(["--add-data", f"{source}{tk.Tcl().call('file', 'normalize', ';')}{dest}"])
    
    command.append(script_path.get())
    return command

def run_pyinstaller():
    command = construct_pyinstaller_command()
    
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "PyInstaller ran successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"PyInstaller failed: {e}")

def select_script():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        script_path.set(file_path)
        update_pyinstaller_command_display()
        if auto_detect_imports_var.get():
            analyze_script_for_imports(file_path)

def analyze_script_for_imports(file_path):
    hidden_imports.clear()
    try:
        with open(file_path, "r") as file:
            content = file.read()
            imports = re.findall(r'^import (\S+)|^from (\S+) import', content, re.MULTILINE)
            for imp in imports:
                module_name = imp[0] if imp[0] else imp[1]
                if module_name not in hidden_imports:
                    hidden_imports.append(module_name)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to analyze script for imports: {e}")
    update_hidden_imports_list()
    update_pyinstaller_command_display()

def update_hidden_imports_list():
    hidden_imports_list.delete(0, tk.END)
    for item in hidden_imports:
        hidden_imports_list.insert(tk.END, item)

# GUI setup
root = tk.Tk()
root.title("PyInstaller GUI")

# Variables
onefile_var = tk.BooleanVar()
windowed_var = tk.BooleanVar()
auto_detect_imports_var = tk.BooleanVar()
hidden_imports = []
add_data = {}
script_path = tk.StringVar()
command_display = tk.StringVar()

# Widgets
tk.Checkbutton(root, text="Onefile", variable=onefile_var, command=update_pyinstaller_command_display).pack(anchor=tk.W)
tk.Checkbutton(root, text="Windowed", variable=windowed_var, command=update_pyinstaller_command_display).pack(anchor=tk.W)
tk.Checkbutton(root, text="Auto-detect imports", variable=auto_detect_imports_var).pack(anchor=tk.W)
tk.Button(root, text="Select Python Script", command=select_script).pack(fill=tk.X)
tk.Entry(root, textvariable=script_path, state='readonly').pack(fill=tk.X)
hidden_imports_list = tk.Listbox(root)
hidden_imports_list.pack(fill=tk.X)
tk.Label(root, textvariable=command_display).pack(fill=tk.X)
tk.Button(root, text="Run PyInstaller", command=run_pyinstaller).pack(fill=tk.X)

update_pyinstaller_command_display()  # Initial command display update

root.mainloop()
