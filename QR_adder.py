import sys
import os
import pandas as pd
import fitz  # PyMuPDF
import qrcode
from io import BytesIO
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QTextEdit, QFileDialog, QGridLayout, QMessageBox, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class QRFormApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('QR Code Adder')

        layout = QVBoxLayout()

        # Form Group
        form_group = QGridLayout()

        # File pickers
        self.template_label = QLabel('Form Template PDF:')
        self.template_path = QLineEdit()
        self.template_browse = QPushButton('Browse')
        self.template_browse.clicked.connect(self.browse_template)

        self.csv_label = QLabel('ID CSV File:')
        self.csv_path = QLineEdit()
        self.csv_browse = QPushButton('Browse')
        self.csv_browse.clicked.connect(self.browse_csv)

        self.output_label = QLabel('Output Folder:')
        self.output_path = QLineEdit()
        self.output_browse = QPushButton('Browse')
        self.output_browse.clicked.connect(self.browse_output)

        # Settings fields
        self.qr_x = QLineEdit('50')
        self.qr_y = QLineEdit('100')
        self.qr_size = QLineEdit('100')
        self.font_size = QLineEdit('12')
        self.text_gap = QLineEdit('5')

        # Connect setting changes to auto-preview
        self.qr_x.textChanged.connect(self.preview_first_entry)
        self.qr_y.textChanged.connect(self.preview_first_entry)
        self.qr_size.textChanged.connect(self.preview_first_entry)
        self.font_size.textChanged.connect(self.preview_first_entry)
        self.text_gap.textChanged.connect(self.preview_first_entry)

        # Preview area
        self.preview_label = QLabel("Preview:")
        self.preview_image = QLabel("No Preview Available")
        self.preview_image.setAlignment(Qt.AlignCenter)
        self.preview_image.setFixedHeight(300)

        # Action buttons
        self.preview_button = QPushButton('Preview First Entry')
        self.preview_button.clicked.connect(self.preview_first_entry)

        self.generate_button = QPushButton('Generate PDFs')
        self.generate_button.clicked.connect(self.generate_pdfs)

        self.help_button = QPushButton('Help')
        self.help_button.clicked.connect(self.show_help)

        self.quit_button = QPushButton('Quit')
        self.quit_button.clicked.connect(QApplication.instance().quit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.quit_button)

        # Progress log
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # Layout arrangement
        form_group.addWidget(self.template_label, 0, 0)
        form_group.addWidget(self.template_path, 0, 1)
        form_group.addWidget(self.template_browse, 0, 2)

        form_group.addWidget(self.csv_label, 1, 0)
        form_group.addWidget(self.csv_path, 1, 1)
        form_group.addWidget(self.csv_browse, 1, 2)

        form_group.addWidget(self.output_label, 2, 0)
        form_group.addWidget(self.output_path, 2, 1)
        form_group.addWidget(self.output_browse, 2, 2)

        form_group.addWidget(QLabel('QR X:'), 3, 0)
        form_group.addWidget(self.qr_x, 3, 1)

        form_group.addWidget(QLabel('QR Y:'), 4, 0)
        form_group.addWidget(self.qr_y, 4, 1)

        form_group.addWidget(QLabel('QR Size:'), 5, 0)
        form_group.addWidget(self.qr_size, 5, 1)

        form_group.addWidget(QLabel('Font Size:'), 6, 0)
        form_group.addWidget(self.font_size, 6, 1)

        form_group.addWidget(QLabel('Text Gap:'), 7, 0)
        form_group.addWidget(self.text_gap, 7, 1)

        layout.addLayout(form_group)
        layout.addWidget(self.preview_label)
        layout.addWidget(self.preview_image)
        layout.addLayout(button_layout)
        layout.addWidget(self.log)

        self.setLayout(layout)
        self.resize(700, 850)

    def browse_template(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Select Form Template PDF', '', 'PDF Files (*.pdf)')
        if file:
            self.template_path.setText(file)
            self.preview_first_entry()

    def browse_csv(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if file:
            self.csv_path.setText(file)
            self.preview_first_entry()

    def browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        if folder:
            self.output_path.setText(folder)

    def show_help(self):
        help_text = (
            "Instructions:\n"
            "1. Select a form template PDF file.\n"
            "2. Select a CSV file with an 'ID' column.\n"
            "3. Select an output folder.\n"
            "4. Adjust QR code placement settings if needed.\n"
            "5. Click 'Preview First Entry' to see a sample.\n"
            "6. Click 'Generate PDFs' to create the combined file.\n"
            "7. Click 'Quit' to exit the application."
        )
        QMessageBox.information(self, 'Help', help_text)

    def log_message(self, message):
        self.log.append(message)
        self.log.repaint()

    def preview_first_entry(self):
        csv_file = self.csv_path.text()
        if not os.path.exists(csv_file):
            self.preview_image.setText("No Preview Available")
            return

        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.strip()

        if len(df) > 0:
            self.show_preview(str(df.iloc[0]['ID']))

    def show_preview(self, id_number):
        template_file = self.template_path.text()

        if not os.path.exists(template_file):
            self.preview_image.setText("No Preview Available")
            return

        try:
            qr_x = float(self.qr_x.text())
            qr_y = float(self.qr_y.text())
            qr_size = float(self.qr_size.text())
            font_size = float(self.font_size.text())
            text_gap = float(self.text_gap.text())
        except ValueError:
            self.preview_image.setText("No Preview Available")
            return

        qr = qrcode.make(id_number)
        qr_byte_arr = BytesIO()
        qr.save(qr_byte_arr, format='PNG')
        qr_byte_arr.seek(0)

        doc = fitz.open(template_file)
        page = doc[0]

        rect_qr = fitz.Rect(qr_x, qr_y, qr_x + qr_size, qr_y + qr_size)
        page.insert_image(rect_qr, stream=qr_byte_arr)

        font = fitz.Font(fontname="helv")
        qr_center_x = (rect_qr.x0 + rect_qr.x1) / 2
        text_width = font.text_length(id_number, fontsize=font_size)
        text_x = qr_center_x - (text_width / 2)
        text_y = rect_qr.y1 + text_gap

        page.insert_text((text_x, text_y), id_number, fontsize=font_size, fontname="helv")

        pix = page.get_pixmap(dpi=150, colorspace=fitz.csRGB)
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        self.preview_image.setPixmap(QPixmap.fromImage(img).scaled(
            self.preview_image.width(),
            self.preview_image.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

        doc.close()

    def generate_pdfs(self):
        template_file = self.template_path.text()
        csv_file = self.csv_path.text()
        output_folder = self.output_path.text()

        if not os.path.exists(template_file) or not os.path.exists(csv_file) or not os.path.isdir(output_folder):
            QMessageBox.critical(self, 'Error', 'Please select valid template, CSV file, and output folder.')
            return

        try:
            qr_x = float(self.qr_x.text())
            qr_y = float(self.qr_y.text())
            qr_size = float(self.qr_size.text())
            font_size = float(self.font_size.text())
            text_gap = float(self.text_gap.text())
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Settings must be numbers.')
            return

        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.strip()

        output_pdf = fitz.open()
        self.log_message("Starting PDF generation...")

        for idx, row in df.iterrows():
            id_number = str(row['ID'])

            qr = qrcode.make(id_number)
            qr_byte_arr = BytesIO()
            qr.save(qr_byte_arr, format='PNG')
            qr_byte_arr.seek(0)

            doc = fitz.open(template_file)
            page = doc[0]

            rect_qr = fitz.Rect(qr_x, qr_y, qr_x + qr_size, qr_y + qr_size)
            page.insert_image(rect_qr, stream=qr_byte_arr)

            font = fitz.Font(fontname="helv")
            qr_center_x = (rect_qr.x0 + rect_qr.x1) / 2
            text_width = font.text_length(id_number, fontsize=font_size)
            text_x = qr_center_x - (text_width / 2)
            text_y = rect_qr.y1 + text_gap

            page.insert_text((text_x, text_y), id_number, fontsize=font_size, fontname="helv")

            output_pdf.insert_pdf(doc)
            doc.close()

            self.log_message(f"[{idx+1}/{len(df)}] Processed ID {id_number}")

        final_path = os.path.join(output_folder, 'all_forms_combined.pdf')
        output_pdf.save(final_path)
        output_pdf.close()

        self.log_message("PDF generation completed.")
        QMessageBox.information(self, 'Done', f'All forms generated and saved at:\n{final_path}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QRFormApp()
    window.show()
    sys.exit(app.exec_())
