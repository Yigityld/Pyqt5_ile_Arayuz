#import socket
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QFrame, QGridLayout, QCheckBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont
from functools import partial
#import serial
import socket
"""
host = "192.168.4.1"
port = 80
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
"""
class WebcamApp(QWidget):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Webcam App")

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas_width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.canvas_height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.label = QLabel(self)
        self.label.setFixedSize(int(self.canvas_width), int(self.canvas_height))

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        slider_style = """
            QSlider::groove:horizontal {
                border: none;
                height: 8px;
                background: #D3D3D3;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #2196F3;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: none;
            }
            QSlider::handle:horizontal {
                background: #FFF;
                border: 1px solid #2196F3;
                width: 18px;
                height: 18px;
                margin: -5px 0; 
                border-radius: 9px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            }
            QSlider::groove:vertical {
                border: none;
                width: 8px;
                background: #D3D3D3;
                border-radius: 4px;
            }
            QSlider::sub-page:vertical {
                background: #2196F3;
                border-radius: 4px;
            }
            QSlider::add-page:vertical {
                background: none;
            }
            QSlider::handle:vertical {
                background: #FFF;
                border: 1px solid #2196F3;
                width: 18px;
                height: 18px;
                margin: 0 -5px; 
                border-radius: 9px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            }
        """

        self.width_slider = QSlider(Qt.Vertical, self)
        self.width_slider.setStyleSheet(slider_style)
        self.width_slider.setRange(480, 640)
        self.width_slider.setValue(640)
        self.width_slider.sliderReleased.connect(self.on_slider_value_changed)
        self.width_slider.setFixedWidth(100)
        self.height_slider = QSlider(Qt.Vertical, self)
        self.height_slider.setRange(320, 480)
        self.height_slider.setValue(480)
        self.height_slider.setStyleSheet(slider_style)
        self.height_slider.setFixedWidth(100)
        self.height_slider.sliderReleased.connect(self.on_slider_value_changed)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.width_slider)
        h_layout.addWidget(self.height_slider)
        MODERN_BUTTON_STYLE = """
                       QPushButton {
                           background-color: #262626;
                           color: white;
                           border: none;
                           border-radius: 8px;
                           padding: 8px 16px;
                           font-size: 14px;
                           font-weight: bold;
                           box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3);
                           transition: background-color 0.3s, transform 0.2s;
                       }
                       QPushButton:hover {
                           background-color: #1a1a1a;
                       }
                       QPushButton:pressed {
                           background-color: #0d0d0d;
                           transform: translateY(2px);
                           box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.2);
                       }
                   """

        layout.addLayout(h_layout)

        self.btn_start = QPushButton("Webcam Aç", self)
        self.btn_start.setStyleSheet(MODERN_BUTTON_STYLE)
        self.btn_start.clicked.connect(self.open_webcam)
        layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("Webcam Kapat", self)
        self.btn_stop.setStyleSheet(MODERN_BUTTON_STYLE)
        self.btn_stop.clicked.connect(self.close_webcam)
        layout.addWidget(self.btn_stop)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)

    def open_webcam(self):
        self.timer.start(15)
        message = "Webcam Açıldı"
        #client.sendall(message.encode('utf-8'))
        #response = client.recv(1024).decode('utf-8')
        print("Sunucudan gelen yanıt:", message)
        #if socket.timeout:
            #print("HAta")


    def close_webcam(self):
        self.timer.stop()
        message = "Webcam Kapandı"
        #client.sendall(message.encode('utf-8'))
        #response = client.recv(1024).decode('utf-8')
        print("Sunucudan gelen yanıt:", message)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.resize(frame, (int(self.width_slider.value()), int(self.height_slider.value())))
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image.rgbSwapped())
            self.label.setPixmap(pixmap)

    def on_slider_value_changed(self):
        width = self.width_slider.value()
        height = self.height_slider.value()
        message = f"Width: {width}, Height: {height}"
        #client.sendall(message.encode('utf-8'))
        print(message)
        #response = client.recv(1024).decode('utf-8')
        #print("Sunucudan gelen yanıt:", response)



class Apps(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Değer Seçimi")
        self.resize(900, 600)

        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        central_widget.setStyleSheet("background-color: #484848;")

        self.slider_references = []
        button_values = [("on", "off"), ("yes", "no"), ("evet", "hayır"), ("açık", "kapalı")]
        slider_labels = ["yaw", "roll", "pitch", "kalibrasyon","deneme","araba"]
        button_headings = ["Taram yap", "Araştır", "Uçak ara", "İleri dönüş yap"]
        slider_style = """
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                height: 10px;
                background: #f2f2f2;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #2196F3, stop: 1 #2196F3);
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #d3d7d9;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #eee;
                border: 1px solid #ccc;
                width: 18px;
                margin: -5px 0;
                border-radius: 8px;
            }
        """
        MODERN_BUTTON_STYLE = """
            QPushButton {
                background-color: #262626;
                color: black;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3);
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
            }
            QPushButton:pressed {
                background-color: #0d0d0d;
                transform: translateY(2px);
                box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.2);
            }
        """


        main_h_layout = QHBoxLayout()
        center_v_layout = QVBoxLayout()


        speed_label = QLabel("Hız", self)
        speed_label.setAlignment(Qt.AlignCenter)
        center_v_layout.addWidget(speed_label)
        self.speed_slider = QSlider(Qt.Vertical, self)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setTickInterval(10)
        self.speed_slider.setValue(50)
        self.speed_slider.setTickPosition(QSlider.TicksLeft)
        self.speed_slider.setStyleSheet(slider_style)
        self.speed_slider.sliderReleased.connect(self.on_speed_slider_changed)
        center_v_layout.addWidget(self.speed_slider)

        font = QFont()
        font.setPointSize(14)

        self.checkbox1 = QCheckBox("Sola Dön X ekseni")
        self.checkbox1.stateChanged.connect(lambda: self.checkbox_checked(self.checkbox1, "1. checkbox onaylandı"))
        self.checkbox1.setFont(font)
        center_v_layout.addWidget(self.checkbox1)

        self.checkbox2 = QCheckBox("Sola Dön Y ekseni")
        self.checkbox2.stateChanged.connect(lambda: self.checkbox_checked(self.checkbox2, "2. checkbox onaylandı"))
        self.checkbox2.setFont(font)
        center_v_layout.addWidget(self.checkbox2)

        self.checkbox3 = QCheckBox("Sola Dön Z ekseni")
        self.checkbox3.stateChanged.connect(lambda: self.checkbox_checked(self.checkbox3, "3. checkbox onaylandı"))
        self.checkbox3.setFont(font)

        center_v_layout.addWidget(self.checkbox3)

        self.setLayout(center_v_layout)

        main_h_layout.addLayout(center_v_layout)

        button_v_layout = QVBoxLayout()
        button_v_layout.setSpacing(75)
        button_v_layout.setContentsMargins(0, 150, 150, 150)

        for index, (val1, val2) in enumerate(button_values):
            h_layout = QHBoxLayout()

            button_label = QLabel(button_headings[index], self)
            button_label.setAlignment(Qt.AlignRight)
            h_layout.addWidget(button_label)

            button = QPushButton(val1, self)
            button.setStyleSheet(MODERN_BUTTON_STYLE)
            button.clicked.connect(partial(self.toggle_button_value, button, (val1, val2), button_headings[index]))
            h_layout.addWidget(button)
            button_v_layout.addLayout(h_layout)  # Buton düzenini button_v_layout'a ekleyin

        main_h_layout.addLayout(button_v_layout)  # button_v_layout'u ana h_layout'a ekleyin

        # Sliderlar için bir QVBoxLayout oluşturma
        slider_v_layout = QVBoxLayout()

        for label_name in slider_labels:
            # Slider için bir dikey düzen (QVBoxLayout) oluşturun
            v_layout = QVBoxLayout()

            # Slider etiketini oluştur ve dikey düzene ekleyin
            slider_label = QLabel(label_name, self)
            slider_label.setAlignment(Qt.AlignCenter)  # Etiketi merkeze hizala
            v_layout.addWidget(slider_label)
            slider = QSlider(Qt.Horizontal)
            slider.setObjectName(label_name)
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setTickInterval(1)
            slider.setValue(0)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setSingleStep(0)
            slider.setStyleSheet(slider_style)
            slider.setFixedWidth(400)
            self.slider_references.append((slider, label_name))
            slider.sliderReleased.connect(self.on_slider_value_changed)
            v_layout.addWidget(slider)

            slider_v_layout.addLayout(v_layout)  # Ana düzene slider düzenini ekleyin

        main_h_layout.addLayout(slider_v_layout)  # slider_v_layout'u ana h_layout'a ekleyin
        main_layout.addLayout(main_h_layout)

        self.control_button = QPushButton("open kontrol", self)
        self.control_button.clicked.connect(self.open_control)
        self.control_button.setStyleSheet(MODERN_BUTTON_STYLE)
        main_layout.addWidget(self.control_button)

        self.setCentralWidget(central_widget)
        self.webcam_window = None
    """
    def receive_response(self, timeout):
        original_timeout = client.gettimeout()
        client.settimeout(timeout)
        try:
              # Zaman aşımı süresini ayarla
            response = client.recv(1024).decode('utf-8')
            return response
        except socket.timeout:
            return None
        finally:
            client.settimeout(0)
    """

    def checkbox_checked(self, cb, message):
        if cb.isChecked():
            print(message)
    def toggle_button_value(self, btn, values, button_heading):
        current_value = btn.text()
        new_value = values[1] if current_value == values[0] else values[0]
        btn.setText(new_value)
        message = f"{button_heading} butonuna basıldı. Yeni değer: {new_value}"
        #client.sendall(message.encode('utf-8'))
        print(message)
        #response = self.receive_response(timeout=1)
        #client.settimeout(2)
        #if response:
           # print("Sunucudan gelen yanıt:", response)
        #else:
            #print("HATA: Sunucudan yanıt alınamadı.")

    def on_speed_slider_changed(self):
        speed_value = self.speed_slider.value()
        message = f"Hız slider değeri değiştirildi. Yeni değer: {speed_value}"
        #client.sendall(message.encode('utf-8'))
        print(message)
        #response = client.recv(1024).decode('utf-8')
        #print("Sunucudan gelen yanıt:", response)

    def on_slider_value_changed(self):
        sender = self.sender()
        if isinstance(sender, QSlider):
            slider_name = sender.objectName()
            value = sender.value()  # değeri bu şekilde alıyoruz
            message = f"{slider_name} slider değeri değiştirildi. Yeni değer: {value}"
            #client.sendall(message.encode('utf-8'))
            print(message)
            #response = client.recv(1024).decode('utf-8')
            #print("Sunucudan gelen yanıt:", response)


    def open_control(self):
        message = "open kontrol butonuna basıldı"
        #client.sendall(message.encode('utf-8'))
        print(message)
        #response = client.recv(1024).decode('utf-8')
        #print("Sunucudan gelen yanıt:", response)
        if not self.webcam_window:
            self.webcam_window = WebcamApp()
            self.webcam_window.show()
        else:
            self.webcam_window.close()
            self.webcam_window = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = Apps()
    mainWin.show()
    sys.exit(app.exec_())
