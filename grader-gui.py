import os
import subprocess
from tkinter import Tk, Button, Frame, Text, messagebox
from tkinter.filedialog import askdirectory
import re

# Fungsi untuk membersihkan ANSI escape sequences dari teks
def remove_ansi_escape_sequences(text):
    # Pola regex untuk mencocokkan ANSI escape sequences
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    # Menghapus ANSI escape sequences dari teks
    return ansi_escape.sub('', text)

# Fungsi untuk menjalankan perintah grader-cli login
def login(result_text):
    result_text.config(state="normal")  # Mengaktifkan kembali area teks
    result_text.insert("end", "Logging in...\n")
    result = subprocess.run(["grader-cli", "login"], capture_output=True, text=True, shell=True)
    result_text.insert("end", remove_ansi_escape_sequences(result.stdout) + "\n")
    result_text.config(state="disabled")  # Menonaktifkan area teks kembali setelah selesai

# Fungsi untuk menjalankan perintah grader-cli group my-group
def my_group(result_text):
    result_text.config(state="normal")  # Mengaktifkan kembali area teks
    result_text.insert("end", "Fetching group information...\n")
    result = subprocess.run(["grader-cli", "group", "my-group"], capture_output=True, text=True, shell=True)
    result_text.insert("end", remove_ansi_escape_sequences(result.stdout) + "\n")
    result_text.config(state="disabled")  # Menonaktifkan area teks kembali setelah selesai

# Fungsi untuk menjalankan perintah grader-cli test
def test_program(result_text):
    result_text.config(state="normal")  # Mengaktifkan kembali area teks
    result_text.insert("end", "Testing program...\n")
    result = subprocess.run(["grader-cli", "test"], capture_output=True, text=True, shell=True)
    result_text.insert("end", remove_ansi_escape_sequences(result.stdout) + "\n")
    result_text.config(state="disabled")  # Menonaktifkan area teks kembali setelah selesai

# Fungsi untuk menjalankan perintah grader-cli submit
def submit_program(result_text):
    result_text.config(state="normal")  # Mengaktifkan kembali area teks
    result_text.insert("end", "Submitting program...\n")
    result = subprocess.run(["grader-cli", "submit"], capture_output=True, text=True, shell=True)
    result_text.insert("end", remove_ansi_escape_sequences(result.stdout) + "\n")
    result_text.config(state="disabled")  # Menonaktifkan area teks kembali setelah selesai

# Fungsi untuk membuka VS Code pada direktori saat ini
def open_vscode(result_text):
    result_text.config(state="normal")  # Mengaktifkan kembali area teks
    result_text.insert("end", "Opening Visual Studio Code...\n")
    result = subprocess.run(["code", "."], capture_output=True, text=True, shell=True)
    result_text.insert("end", remove_ansi_escape_sequences(result.stdout) + "\n")
    result_text.config(state="disabled")  # Menonaktifkan area teks kembali setelah selesai
    
# Fungsi untuk membuka File Explorer dan memilih direktori
def choose_directory():
    root = Tk()
    root.withdraw()  # Menyembunyikan jendela root Tkinter yang tidak diperlukan
    directory = askdirectory(title="Pilih Direktori")
    return directory

# Fungsi untuk mengubah direktori
def change_directory():
    directory = choose_directory()
    if directory:
        os.chdir(directory)
        messagebox.showinfo("Change Directory", f"Direktori berhasil diubah ke: {directory}")

# Fungsi untuk mendapatkan dan menampilkan direktori saat ini
def show_current_directory():
    current_directory = os.getcwd()
    messagebox.showinfo("Current Directory", f"Direktori saat ini: {current_directory}")

# Fungsi untuk membuat dan menampilkan tombol-tombol
def create_buttons():
    root = Tk()
    root.title("Menu")

    # Frame untuk mengelompokkan tombol-tombol
    button_frame = Frame(root)
    button_frame.pack(side="left", fill="y", padx=(20, 0), pady=20) # Menambahkan padding dari kanan dan bawah

    # Tombol untuk mengubah direktori
    change_dir_button = Button(button_frame, text="Change Directory", command=change_directory, width=20, height=2)
    change_dir_button.pack(pady=5)

    # Tombol untuk menampilkan direktori saat ini
    show_dir_button = Button(button_frame, text="Show Directory", command=show_current_directory, width=20, height=2)
    show_dir_button.pack(pady=5)

    # Tombol untuk login
    login_button = Button(button_frame, text="Login", command=lambda: login(result_text), width=20, height=2)
    login_button.pack(pady=5)

    # Tombol untuk my group
    my_group_button = Button(button_frame, text="My Group", command=lambda: my_group(result_text), width=20, height=2)
    my_group_button.pack(pady=5)

    # Tombol untuk test program
    test_button = Button(button_frame, text="Test Program", command=lambda: test_program(result_text), width=20, height=2)
    test_button.pack(pady=5)

    # Tombol untuk submit program
    submit_button = Button(button_frame, text="Submit Program", command=lambda: submit_program(result_text), width=20, height=2)
    submit_button.pack(pady=5)

    # Tombol untuk membuka VS Code
    open_vscode_button = Button(button_frame, text="Open VS Code", command=lambda: open_vscode(result_text), width=20, height=2)
    open_vscode_button.pack(pady=5)

    # Area teks untuk menampilkan hasil subprocess terminal
    result_text = Text(root, height=10, width=60, state="disabled")  # Menentukan state menjadi "disabled"
    result_text.pack(side="left", fill="both", expand=True, padx=20, pady=20)  # Menggunakan pack dengan opsi fill dan expand

    # Menambahkan padding di dalam area teks
    result_text.configure(padx=10, pady=10)

    # Menambahkan teks copyright
    result_text.insert("end", "\nDeveloped by farismnrr")

    # Handler untuk event close window
    def on_closing():
        root.quit()  # Menghentikan mainloop
        root.destroy()  # Menutup jendela Tkinter saat program dihentikan

    root.protocol("WM_DELETE_WINDOW", on_closing)  # Menambahkan handler untuk event close window

    root.mainloop()

if __name__ == "__main__":
    create_buttons()