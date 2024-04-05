import os
import subprocess
import threading
from tkinter import Tk, Button, Frame, Text, messagebox, simpledialog
from tkinter.filedialog import askdirectory
import re, time

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
def test_program_grader(result_text):
    result_text.config(state="normal")  # Mengaktifkan kembali area teks
    result_text.insert("end", "Testing program with grader...\n")
    result = subprocess.run(["grader-cli", "test"], capture_output=True, text=True, shell=True)
    result_text.insert("end", remove_ansi_escape_sequences(result.stdout) + "\n")
    result_text.config(state="disabled")  # Menonaktifkan area teks kembali setelah selesai

def test_program_golang(result_text):
    result_text.config(state="normal")  # Mengaktifkan kembali area teks
    result_text.insert("end", "Testing golang program...\n")
    
    # Membuka proses dan mengeksekusi perintah "go run main.go"
    process = subprocess.Popen(["go", "run", "main.go"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Menampilkan output dari proses
    stdout, stderr = process.communicate()
    result_text.insert("end", stdout)
    result_text.insert("end", stderr)
    
    result_text.insert("end", "Program telah dijalankan.\n")
    result_text.config(state="disabled")  # Menonaktifkan area teks kembali setelah selesai
    
def test_program_golang_terminal(result_text):
    result_text.config(state="normal")
    result_text.insert("end", "Testing program with golang...\n")

    try:
        # Membuka PowerShell di jendela baru dan menyimpan id prosesnya
        subprocess.Popen(["powershell", "-Command", "start-process", "powershell", "-ArgumentList", "'-NoExit','-Command','go run main.go'"], shell=True)
        
        result_text.insert("end", "Program execution completed.\n")
    except subprocess.CalledProcessError as e:
        result_text.insert("end", f"Error: {e}\n")

    result_text.config(state="disabled") # Menonaktifkan area teks kembali setelah selesai

# Fungsi untuk menjalankan perintah grader-cli submit
def submit_program(result_text):
    result_text.config(state="normal")  # Mengaktifkan kembali area teks
    result_text.insert("end", "Submitting program...\n")
    result = subprocess.run(["grader-cli", "submit"], capture_output=True, text=True, shell=True)
    result_text.insert("end", remove_ansi_escape_sequences(result.stdout) + "\n")
    result_text.config(state="disabled")  # Menonaktifkan area teks kembali setelah selesai

# Fungsi untuk mengeksekusi perintah pull assignment
def pull_assignment(result_text):
    # Meminta input dari pengguna
    assignment_name = simpledialog.askstring("Pull Assignment", "Masukkan nama assignment:")
    if assignment_name is not None and assignment_name.strip():  # Validasi teks tidak kosong
        # Mengonfigurasi teks untuk hasil
        result_text.config(state="normal")  # Mengaktifkan area teks
        result_text.insert("end", f"Pulling assignment: {assignment_name}\n")
        
        # Memeriksa apakah input adalah URL
        if assignment_name.startswith("https://dendrite.ruangguru.com/asg/"):
            # Menghapus bagian URL yang tidak relevan
            assignment_name = assignment_name.replace("https://dendrite.ruangguru.com/asg/", "")
        
        # Menjalankan perintah grader-cli assignment pull
        result = subprocess.run(["grader-cli", "assignment", "pull", assignment_name], capture_output=True, text=True, shell=True)
        
        # Memasukkan hasil perintah ke dalam area teks
        result_text.insert("end", remove_ansi_escape_sequences(result.stdout) + "\n")
        result_text.config(state="disabled")  # Menonaktifkan area teks kembali setelah selesai
    elif assignment_name == "":  # Menangani kasus ketika pengguna membatalkan dialog
        # Jika pengguna membatalkan input, tampilkan pesan
        messagebox.showinfo("Info", "Input tidak boleh kosong.")
    else:
        # Jika pengguna membatalkan input, tampilkan pesan
        messagebox.showinfo("Info", "Operasi dibatalkan.")

def clear_terminal(result_text):
    # Mengaktifkan kembali area teks
    result_text.config(state="normal")
    
    # Menghapus seluruh teks dari awal sampai akhir
    result_text.delete("1.0", "end")
    
    # Menonaktifkan area teks kembali setelah selesai
    result_text.config(state="disabled")

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

# Fungsi untuk membuat tombol-tombol
def create_buttons():
    root = Tk()
    root.title("Grader GUI")
    root.iconbitmap('./icon.ico')

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

    # Tombol untuk test program with grader
    test_button = Button(button_frame, text="Test Program (Grader)", command=lambda: test_program_grader(result_text), width=20, height=2)
    test_button.pack(pady=5)
    
    # Tombol untuk test program with golang
    test_button = Button(button_frame, text="Test Program (Golang)", command=lambda: test_program_golang(result_text), width=20, height=2)
    test_button.pack(pady=5)

    # Tombol untuk test program with golang terminal
    test_button = Button(button_frame, text="Test Program (Terminal)", command=lambda: test_program_golang_terminal(result_text), width=20, height=2)
    test_button.pack(pady=5)
    
    # Tombol untuk submit program
    submit_button = Button(button_frame, text="Submit Program", command=lambda: submit_program(result_text), width=20, height=2)
    submit_button.pack(pady=5)

    # Tombol untuk pull assignment
    pull_assignment_button = Button(button_frame, text="Pull Assignment", command=lambda: pull_assignment(result_text), width=20, height=2)
    pull_assignment_button.pack(pady=5)

    # Tombol untuk menghapus text pada console
    clear_terminal_botton = Button(button_frame, text="Clear Console", command=lambda: clear_terminal(result_text), width=20, height=2)
    clear_terminal_botton.pack(pady=5)
    
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
