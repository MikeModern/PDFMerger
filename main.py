import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QListWidget, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QIcon

from PyPDF2 import PdfMerger

class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Merger - Mike van Doesburg")
        self.setGeometry(100, 100, 800, 400)
        self.setAcceptDrops(True)

        self.file_list = []

        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.label = QLabel("Sleep hier twee of meer bestanden om ze samen te voegen.")
        layout.addWidget(self.label)

        self.file_listbox = QListWidget()
        layout.addWidget(self.file_listbox)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        self.delete_button = QPushButton("Verwijder")
        self.delete_button.clicked.connect(self.remove_file)
        button_layout.addWidget(self.delete_button)

        self.merge_button = QPushButton("Samenvoegen")
        self.merge_button.clicked.connect(self.on_merge_click)
        button_layout.addWidget(self.merge_button)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        files = [url.toLocalFile() for url in urls]
        for file in files:
            if file.lower().endswith('.pdf') and file not in self.file_list:
                self.file_list.append(file)
                self.update_file_listbox()

    def update_file_listbox(self):
        self.file_listbox.clear()
        self.file_listbox.addItems(self.file_list)

    def remove_file(self):
        selected_items = self.file_listbox.selectedItems()
        if selected_items:
            item = selected_items[0]
            self.file_list.remove(item.text())
            self.update_file_listbox()

    def clear_file_list(self):
        self.file_list.clear()
        self.update_file_listbox()

    def on_merge_click(self):
        if len(self.file_list) >= 2:
            self.merge_pdfs()
        else:
            QMessageBox.critical(self, "Fout", "Zorg ervoor dat er minstens 2 bestanden zijn om te combineren.")

    def merge_pdfs(self):
        merger = PdfMerger()
        pdfs = [file for file in self.file_list if file.lower().endswith('.pdf')]

        output_path, _ = QFileDialog.getSaveFileName(self, "Opslaan als", "", "PDF files (*.pdf);;All Files (*)")
        if output_path and pdfs:
            for pdf_file in pdfs:
                merger.append(pdf_file)

            merger.write(output_path)
            merger.close()
            QMessageBox.information(self, "Succes", f"Bestanden zijn samengevoegd en opgeslagen als {output_path}")
            self.clear_file_list()
        else:
            QMessageBox.warning(self, "Annuleren", "Opslaan geannuleerd.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec_())
