package main

import (
	"fyne.io/fyne/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	// Inisialisasi aplikasi Fyne
	myApp := app.New()

	// Membuat window
	myWindow := myApp.NewWindow("Contoh GUI Sederhana")

	// Membuat widget teks
	welcome := widget.NewLabel("Selamat datang di Program GUI Sederhana dengan Golang!")

	// Membuat tombol
	myButton := widget.NewButton("Klik Saya", func() {
		welcome.SetText("Tombol telah diklik!")
	})

	// Menata widget dalam kontainer
	content := container.NewVBox(
		welcome,
		myButton,
	)

	// Menambahkan konten ke window
	myWindow.SetContent(content)

	// Menampilkan window
	myWindow.ShowAndRun()
}
