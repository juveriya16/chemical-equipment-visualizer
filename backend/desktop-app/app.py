import sys
import webbrowser
import requests
import datetime
import random

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog,
    QVBoxLayout, QLabel, QHBoxLayout, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ================= WORKER THREAD =================
class UploadWorker(QThread):
    success = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            with open(self.file_path, "rb") as f:
                res = requests.post(
                    "http://127.0.0.1:8000/api/upload/",
                    files={"file": f},
                    timeout=10
                )

            if res.status_code == 200:
                self.success.emit(res.json())
            else:
                self.error.emit("Backend error")

        except Exception as e:
            self.error.emit(str(e))


# ================= PIE CHART =================
class PieChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(4.2, 3.8), facecolor="none")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("none")
        super().__init__(self.fig)

    def plot(self, data):
        self.ax.clear()
        self.ax.pie(
            data.values(),
            labels=data.keys(),
            autopct="%1.1f%%",
            startangle=140,
            explode=[0.05] * len(data),
            colors=["#a855f7", "#6366f1", "#22d3ee"],
            shadow=True
        )
        self.ax.set_title("Equipment Distribution", fontsize=14, color="white", pad=14)
        self.ax.axis("equal")
        self.draw()


# ================= LINE CHART =================
class LineChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(4.2, 3.8), facecolor="none")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("none")
        super().__init__(self.fig)

    def plot(self):
        self.ax.clear()
        x = list(range(1, 8))
        y = [random.randint(90, 150) for _ in x]

        self.ax.plot(x, y, color="#22d3ee", linewidth=3, marker="o")
        self.ax.fill_between(x, y, color="#22d3ee", alpha=0.15)
        self.ax.set_title("Flowrate Trend", fontsize=14, color="white", pad=14)
        self.ax.tick_params(colors="white")
        self.draw()


# ================= MAIN WINDOW =================
class DesktopAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Desktop Analyzer")
        self.setGeometry(120, 80, 1100, 640)
        self.setStyleSheet(self.styles())

        # HEADER
        title = QLabel("Chemical Equipment Analyzer")
        title.setObjectName("title")

        upload_btn = QPushButton("Upload CSV")
        upload_btn.clicked.connect(self.upload_csv)

        self.pdf_btn = QPushButton("Download PDF")
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.pdf_btn.setEnabled(False)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_data)

        header = QHBoxLayout()
        header.addWidget(title)
        header.addStretch()
        header.addWidget(upload_btn)
        header.addWidget(self.pdf_btn)
        header.addWidget(clear_btn)

        # STATUS
        self.status = QLabel("Upload a CSV file to begin")
        self.file_info = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        self.file_info.setAlignment(Qt.AlignCenter)

        # KPI LABELS
        self.total = QLabel("–")
        self.flow = QLabel("–")
        self.pressure = QLabel("–")
        self.temp = QLabel("–")

        cards = QHBoxLayout()
        for lbl in [self.total, self.flow, self.pressure, self.temp]:
            cards.addWidget(self.card(lbl))

        # CHARTS
        self.pie = PieChart()
        self.line = LineChart()

        charts = QHBoxLayout()
        charts.addWidget(self.panel(self.pie))
        charts.addWidget(self.panel(self.line))

        # MAIN LAYOUT
        main = QVBoxLayout()
        main.addLayout(header)
        main.addWidget(self.status)
        main.addWidget(self.file_info)
        main.addLayout(cards)
        main.addLayout(charts)

        self.setLayout(main)
        self.worker = None


    # ================= FUNCTIONS =================
    def upload_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)", options=options
        )

        if not file_path:
            return

        self.status.setText("Uploading…")
        self.worker = UploadWorker(file_path)
        self.worker.success.connect(lambda d: self.show_result(d, file_path))
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def show_result(self, data, file_path):
        time = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")

        self.status.setText("Uploaded Successfully ✔")
        self.file_info.setText(f"File: {file_path.split('/')[-1]} | Uploaded at: {time}")
        self.pdf_btn.setEnabled(True)

        self.total.setText(self.kpi("Total", data.get("total_count", 0)))
        self.flow.setText(self.kpi("Avg Flowrate", round(data.get("avg_flowrate", 0), 2)))
        self.pressure.setText(self.kpi("Avg Pressure", round(data.get("avg_pressure", 0), 2)))
        self.temp.setText(self.kpi("Avg Temperature", round(data.get("avg_temperature", 0), 2)))

        if "type_distribution" in data:
            self.pie.plot(data["type_distribution"])

        self.line.plot()

    def clear_data(self):
        self.status.setText("Upload a CSV file to begin")
        self.file_info.setText("")
        self.pdf_btn.setEnabled(False)

        for lbl in [self.total, self.flow, self.pressure, self.temp]:
            lbl.setText("–")

        self.pie.ax.clear()
        self.line.ax.clear()
        self.pie.draw()
        self.line.draw()

    def download_pdf(self):
        webbrowser.open("http://127.0.0.1:8000/api/report/pdf/")

    def show_error(self, msg):
        QMessageBox.critical(self, "Error", msg)

    def kpi(self, title, value):
        return (
            f"<div style='font-size:14px;color:#e9d5ff'>{title}</div>"
            f"<div style='font-size:32px;font-weight:800;margin-top:6px'>{value}</div>"
        )

    def card(self, label):
        frame = QFrame()
        frame.setObjectName("card")

        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(frame)
        layout.addStretch()        # 🔑 TOP SPACE
        layout.addWidget(label)
        layout.addStretch()        # 🔑 BOTTOM SPACE

        return frame

    def panel(self, widget):
        frame = QFrame()
        frame.setObjectName("panel")
        layout = QVBoxLayout(frame)
        layout.addWidget(widget)
        return frame

    def styles(self):
        return """
        QWidget {
            background: qlineargradient(
                x1:0,y1:0,x2:1,y2:1,
                stop:0 #0b061a,
                stop:1 #1b0f3a
            );
            color: white;
            font-family: Segoe UI;
        }

        #title {
            font-size: 26px;
            font-weight: 700;
            color: #f5f3ff;
        }

        QPushButton {
            background: qlineargradient(
                x1:0,y1:0,x2:1,y2:0,
                stop:0 #7c5cff,
                stop:1 #a78bfa
            );
            border-radius: 16px;
            padding: 9px 20px;
            font-size: 14px;
        }

        #card {
            background: rgba(124,92,255,0.30);
            border-radius: 24px;
            min-width: 190px;
            min-height: 120px;
        }

        #card:hover {
            background: rgba(236,72,153,0.50);
            box-shadow: 0 0 30px rgba(139,92,246,1.0);
        }

        #panel {
            background: rgba(124,92,255,0.18);
            border-radius: 20px;
            padding: 14px;
        }
        """


# ================= RUN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopAnalyzer()
    window.show()
    sys.exit(app.exec())
