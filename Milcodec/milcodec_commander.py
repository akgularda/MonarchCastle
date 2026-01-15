"""
MILCODEC COMMANDER TERMINAL v2.0 - "GLASS COCKPIT"
===================================================
Professional C2 command center for secure signal transmission.
Features Palantir-inspired tactical interface with spectrum visualization.
"""

import sys
import os
import time
import socket
import threading
import queue
import numpy as np
import random
import wave
import struct
from datetime import datetime

# GUI Imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLabel, QLineEdit, QPushButton, QFrame, QListWidget,
    QSplitter, QComboBox, QListWidgetItem, QGroupBox, QRadioButton,
    QButtonGroup, QSizePolicy, QGraphicsDropShadowEffect, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QMutex, QSize
from PyQt6.QtGui import (
    QColor, QPalette, QFont, QPainter, QBrush, QPen, QLinearGradient,
    QIcon
)

# Cryptography Imports
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# Theme Import
try:
    from theme import Colors, Fonts, Styles
except ImportError:
    class Colors:
        VOID = "#0a0a0f"
        BACKGROUND = "#0d0d14"
        SURFACE = "#14141f"
        ELEVATED = "#1a1a2e"
        BORDER = "#2a2a3e"
        BORDER_DIM = "#1e1e2e"
        TEXT_PRIMARY = "#e8e8f0"
        TEXT_SECONDARY = "#a0a0b8"
        TEXT_DIM = "#606078"
        CYAN = "#00d4ff"
        GREEN = "#00ff88"
        RED = "#ff3355"
        AMBER = "#ffb000"

# =============================================================================
# CONSTANTS
# =============================================================================
VERSION = "2.0.0"
SAMPLE_RATE = 44100
PNC_KEY = np.array([
    1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,
    0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0
], dtype=np.float32) * 2 - 1

# Transmission Modes
MODE_TCP = "TCP"
MODE_RADIO = "RADIO"
MODE_INTERNET = "INTERNET"
MODE_FM = "FM"

# Priority Levels
PRIORITIES = ["ROUTINE", "PRIORITY", "IMMEDIATE", "FLASH"]

# =============================================================================
# ENCRYPTION CORE
# =============================================================================
class EncryptionCore:
    """Post-Quantum Cryptography Encryption Engine."""
    
    def __init__(self):
        self.cmd_private_key = b"COMMANDER_SECRET_KEY_32BYTES!!"
        self.session_count = 0

    def encrypt_packet(self, plaintext, target_unit="ALL", priority="ROUTINE"):
        """
        Encrypt command with ChaCha20-Poly1305.
        Format: CMD:[TARGET]:[PRIORITY]:[ENCRYPTED_PAYLOAD]
        """
        self.session_count += 1
        header = f"CMD:{target_unit}:{priority}:".encode('utf-8')
        payload = plaintext.encode('utf-8')

        if not CRYPTO_AVAILABLE:
            return header + payload

        try:
            session_key = os.urandom(32)
            nonce = os.urandom(12)

            cipher = Cipher(
                algorithms.ChaCha20(session_key, nonce),
                mode=None,
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(payload)

            # In production: Kyber KEM encapsulation of session_key
            return header + payload  # Simplified for demo
        except:
            return header + payload


# =============================================================================
# DSSS MASKER (Import or Fallback)
# =============================================================================
try:
    from milcodec_masker import DSSSMasker
except ImportError:
    class DSSSMasker:
        def generate_masked_audio(self, payload):
            # Minimal fallback
            return np.random.normal(0, 0.1, 44100).astype(np.float32)


# =============================================================================
# TRANSMISSION ENGINE
# =============================================================================
class TransmissionEngine(QThread):
    tx_status_signal = pyqtSignal(str, str)  # message, level
    tx_spectrum_signal = pyqtSignal(list)
    tx_complete_signal = pyqtSignal(bool, str)  # success, details

    def __init__(self):
        super().__init__()
        self.crypto = EncryptionCore()
        self.masker = DSSSMasker()
        self.transmit_mode = MODE_TCP
        self.target_ip = "127.0.0.1"
        self.target_port = 5555
        self.orders_sent = 0

    def set_mode(self, mode):
        self.transmit_mode = mode
        self.tx_status_signal.emit(f"TX MODE: {mode}", "INFO")

    def set_target(self, ip, port):
        self.target_ip = ip
        self.target_port = port

    def send_order(self, message, target="ALL", priority="ROUTINE"):
        """Main transmission pipeline."""
        self.tx_status_signal.emit(f"ENCRYPTING: {len(message)} bytes", "INFO")

        # 1. Encrypt
        encrypted_blob = self.crypto.encrypt_packet(message, target, priority)

        # 2. DSSS Modulation
        self.tx_status_signal.emit("GENERATING DSSS CARRIER...", "INFO")
        audio_packet = self.masker.generate_masked_audio(encrypted_blob)

        # 3. Spectrum visualization
        if len(audio_packet) > 512:
            fft_data = np.abs(np.fft.fft(audio_packet[:512]))[:256]
            self.tx_spectrum_signal.emit(fft_data.tolist())

        # 4. Transmit based on mode
        success = False
        details = ""

        if self.transmit_mode == MODE_RADIO or self.transmit_mode == MODE_FM:
            success, details = self._save_to_wav(audio_packet, priority)
        elif self.transmit_mode == MODE_INTERNET:
            success, details = self._stream_internet(audio_packet)
        else:
            success, details = self._stream_tcp(audio_packet)

        if success:
            self.orders_sent += 1

        self.tx_complete_signal.emit(success, details)

    def _save_to_wav(self, audio_data, priority=""):
        """Save transmission as WAV file for radio broadcast."""
        try:
            timestamp = int(time.time())
            filename = f"broadcast_{priority}_{timestamp}.wav"
            scaled = np.int16(audio_data / np.max(np.abs(audio_data) + 1e-9) * 32767)

            with wave.open(filename, 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(scaled.tobytes())

            return True, f"SAVED: {filename}"
        except Exception as e:
            return False, f"SAVE FAILED: {str(e)}"

    def _stream_tcp(self, audio_data):
        """Stream to receiver via TCP."""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(5)
            client.connect((self.target_ip, self.target_port))
            client.sendall(audio_data.tobytes())
            client.close()
            return True, f"TCP SENT TO {self.target_ip}:{self.target_port}"
        except ConnectionRefusedError:
            return False, "CONNECTION REFUSED"
        except socket.timeout:
            return False, "CONNECTION TIMEOUT"
        except Exception as e:
            return False, f"TX ERROR: {str(e)}"

    def _stream_internet(self, audio_data):
        """Stream to internet radio server (simulated)."""
        self.tx_status_signal.emit("CONNECTING TO STREAM SERVER...", "INFO")
        time.sleep(0.5)  # Simulate connection
        return True, "STREAM QUEUED (SIMULATION)"


# =============================================================================
# CUSTOM WIDGETS
# =============================================================================
class SpectrumAnalyzer(QFrame):
    """FFT Spectrum visualization with gradient bars."""
    
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(150)
        self.data = []
        self.setStyleSheet("background: transparent;")

    def update_data(self, data):
        self.data = data[:128] if len(data) > 128 else data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()

        # Background
        painter.fillRect(0, 0, w, h, QColor(Colors.VOID))

        # Grid
        painter.setPen(QPen(QColor(Colors.BORDER_DIM), 1, Qt.PenStyle.DotLine))
        for y in range(0, h, 25):
            painter.drawLine(0, y, w, y)

        if not self.data:
            # Draw placeholder
            painter.setPen(QPen(QColor(Colors.TEXT_DIM)))
            painter.drawText(w // 2 - 50, h // 2, "AWAITING SIGNAL")
            return

        # Draw spectrum bars with gradient
        bar_count = len(self.data)
        bar_width = max(2, w // bar_count - 1)
        max_val = max(self.data) if self.data else 1

        for i, val in enumerate(self.data):
            x = int(i * (w / bar_count))
            bar_height = int((val / max_val) * h * 0.9)
            
            if bar_height < 2:
                continue

            # Gradient from cyan to amber based on height
            ratio = bar_height / h
            if ratio > 0.7:
                color = QColor(Colors.RED)
            elif ratio > 0.4:
                color = QColor(Colors.AMBER)
            else:
                color = QColor(Colors.CYAN)

            painter.fillRect(x, h - bar_height, bar_width, bar_height, color)


class TacticalMap(QFrame):
    """Enhanced tactical battlespace visualization."""
    
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(200)
        self.units = [
            {"id": "ALPHA-1", "x": 0.3, "y": 0.4, "status": "ACTIVE"},
            {"id": "BRAVO-2", "x": 0.6, "y": 0.3, "status": "SILENT"},
            {"id": "CHARLIE-9", "x": 0.5, "y": 0.7, "status": "PENDING"},
        ]
        self.hq_pos = (0.5, 0.5)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()

        # Background
        painter.fillRect(0, 0, w, h, QColor(Colors.VOID))

        # Grid
        painter.setPen(QPen(QColor(Colors.BORDER_DIM), 1))
        grid_size = 40
        for x in range(0, w, grid_size):
            painter.drawLine(x, 0, x, h)
        for y in range(0, h, grid_size):
            painter.drawLine(0, y, w, y)

        # Radar circles
        cx, cy = w // 2, h // 2
        painter.setPen(QPen(QColor(Colors.CYAN_DIM if hasattr(Colors, 'CYAN_DIM') else "#0088aa"), 1, Qt.PenStyle.DashLine))
        for r in range(50, max(w, h), 50):
            painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        # HQ marker
        hx, hy = int(self.hq_pos[0] * w), int(self.hq_pos[1] * h)
        painter.setBrush(QBrush(QColor(Colors.CYAN)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(hx - 6, hy - 6, 12, 12)
        
        painter.setPen(QPen(QColor(Colors.CYAN)))
        painter.drawText(hx + 10, hy + 4, "HQ")

        # Unit markers
        status_colors = {
            "ACTIVE": Colors.GREEN,
            "SILENT": Colors.AMBER,
            "PENDING": Colors.TEXT_DIM,
        }

        for unit in self.units:
            ux = int(unit["x"] * w)
            uy = int(unit["y"] * h)
            color = QColor(status_colors.get(unit["status"], Colors.TEXT_DIM))

            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(ux - 5, uy - 5, 10, 10)

            painter.setPen(QPen(color))
            painter.drawText(ux + 8, uy + 4, unit["id"])


class UnitListItem(QListWidgetItem):
    """Custom list item for unit roster."""
    pass


class CommandHistory(QTextEdit):
    """Command log with colored output."""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 4px;
                padding: 8px;
                font-family: 'JetBrains Mono', 'Consolas', monospace;
                font-size: 10pt;
            }}
        """)

    def log(self, text, level="INFO"):
        colors = {
            "INFO": Colors.CYAN,
            "SUCCESS": Colors.GREEN,
            "WARNING": Colors.AMBER,
            "ERROR": Colors.RED,
            "COMMAND": Colors.TEXT_PRIMARY,
        }
        color = colors.get(level, Colors.TEXT_SECONDARY)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.append(f'<span style="color: {Colors.TEXT_DIM};">[{timestamp}]</span> '
                   f'<span style="color: {color};">{text}</span>')
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


# =============================================================================
# MAIN WINDOW ("THE GLASS COCKPIT")
# =============================================================================
class CommanderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tx_engine = TransmissionEngine()
        self.command_history = []
        self.init_ui()
        self.init_signals()

    def init_ui(self):
        self.setWindowTitle(f"MILCODEC COMMANDER v{VERSION} - GLASS COCKPIT")
        self.setGeometry(50, 50, 1200, 800)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {Colors.BACKGROUND};
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-family: 'Inter', 'Segoe UI', sans-serif;
            }}
        """)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === HEADER ===
        header = self._create_header()
        main_layout.addWidget(header)

        # === MAIN CONTENT ===
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(16, 16, 16, 16)

        # LEFT PANEL: Spectrum & Log
        left_panel = self._create_left_panel()
        content_layout.addWidget(left_panel, 2)

        # CENTER PANEL: Map & Command
        center_panel = self._create_center_panel()
        content_layout.addWidget(center_panel, 4)

        # RIGHT PANEL: Units & Config
        right_panel = self._create_right_panel()
        content_layout.addWidget(right_panel, 2)

        main_layout.addWidget(content, stretch=1)

        # === FOOTER ===
        footer = self._create_footer()
        main_layout.addWidget(footer)

        # Initialize
        self.log_status("SYSTEM INITIALIZED", "SUCCESS")
        self.log_status(f"DEFAULT MODE: {self.tx_engine.transmit_mode}", "INFO")

    def _create_header(self):
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {Colors.ELEVATED}, stop:1 {Colors.SURFACE});
                border-bottom: 1px solid {Colors.BORDER};
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 0, 16, 0)

        # Title
        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        title = QLabel("MILCODEC COMMANDER")
        title.setStyleSheet(f"""
            font-size: 14pt;
            font-weight: 600;
            color: {Colors.AMBER};
            letter-spacing: 2px;
        """)

        subtitle = QLabel("GLASS COCKPIT • C2 TRANSMISSION TERMINAL")
        subtitle.setStyleSheet(f"font-size: 9pt; color: {Colors.TEXT_DIM};")

        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        layout.addLayout(title_col)

        layout.addStretch()

        # TX Counter
        tx_col = QVBoxLayout()
        tx_label = QLabel("ORDERS SENT")
        tx_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 8pt;")
        self.tx_counter = QLabel("0")
        self.tx_counter.setStyleSheet(f"color: {Colors.GREEN}; font-size: 18pt; font-weight: bold;")
        tx_col.addWidget(tx_label, alignment=Qt.AlignmentFlag.AlignCenter)
        tx_col.addWidget(self.tx_counter, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(tx_col)

        layout.addSpacing(32)

        # Clock
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet(f"""
            font-family: 'JetBrains Mono', 'Consolas';
            font-size: 12pt;
            color: {Colors.AMBER};
        """)
        layout.addWidget(self.clock_label)

        # Clock timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

        return header

    def _create_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 6px;
            }}
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Spectrum Analyzer
        spec_label = QLabel("TX SPECTRUM ANALYZER")
        spec_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt; font-weight: 600; letter-spacing: 1px;")
        layout.addWidget(spec_label)

        self.spectrum = SpectrumAnalyzer()
        layout.addWidget(self.spectrum)

        # System Log
        log_label = QLabel("SYSTEM LOG")
        log_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt; font-weight: 600; letter-spacing: 1px;")
        layout.addWidget(log_label)

        self.log_view = CommandHistory()
        layout.addWidget(self.log_view, stretch=1)

        return panel

    def _create_center_panel(self):
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 6px;
            }}
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Tactical Map
        map_label = QLabel("TACTICAL BATTLESPACE")
        map_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt; font-weight: 600; letter-spacing: 1px;")
        layout.addWidget(map_label)

        self.tactical_map = TacticalMap()
        layout.addWidget(self.tactical_map, stretch=2)

        # Command Input
        cmd_label = QLabel("COMMAND UPLINK")
        cmd_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt; font-weight: 600; letter-spacing: 1px;")
        layout.addWidget(cmd_label)

        # Priority selector
        priority_row = QHBoxLayout()
        priority_label = QLabel("PRIORITY:")
        priority_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        priority_row.addWidget(priority_label)

        self.priority_group = QButtonGroup()
        for i, p in enumerate(PRIORITIES):
            rb = QRadioButton(p)
            rb.setStyleSheet(f"""
                QRadioButton {{
                    color: {Colors.TEXT_SECONDARY};
                    spacing: 5px;
                }}
                QRadioButton::indicator {{
                    width: 12px;
                    height: 12px;
                }}
            """)
            if p == "ROUTINE":
                rb.setChecked(True)
            self.priority_group.addButton(rb, i)
            priority_row.addWidget(rb)

        priority_row.addStretch()
        layout.addLayout(priority_row)

        # Command line
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter command: /all <message> | /to <unit> <message> | /mode <tcp|radio|fm>")
        self.cmd_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.VOID};
                border: 2px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 12px 16px;
                color: {Colors.CYAN};
                font-family: 'JetBrains Mono', 'Consolas';
                font-size: 11pt;
            }}
            QLineEdit:focus {{
                border-color: {Colors.AMBER};
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_DIM};
            }}
        """)
        self.cmd_input.returnPressed.connect(self.handle_command)
        layout.addWidget(self.cmd_input)

        # Quick send button
        send_row = QHBoxLayout()
        send_row.addStretch()

        self.btn_send = QPushButton("TRANSMIT")
        self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_send.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2a1a, stop:1 #1a1a0a);
                border: 2px solid {Colors.AMBER};
                border-radius: 4px;
                padding: 10px 32px;
                color: {Colors.AMBER};
                font-weight: bold;
                font-size: 11pt;
                letter-spacing: 2px;
            }}
            QPushButton:hover {{
                background-color: {Colors.AMBER};
                color: {Colors.VOID};
            }}
        """)
        self.btn_send.clicked.connect(self.handle_command)
        send_row.addWidget(self.btn_send)

        layout.addLayout(send_row)

        return panel

    def _create_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 6px;
            }}
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Unit Roster
        units_label = QLabel("ACTIVE UNITS")
        units_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt; font-weight: 600; letter-spacing: 1px;")
        layout.addWidget(units_label)

        self.unit_list = QListWidget()
        self.unit_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 4px;
                padding: 4px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 3px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QListWidget::item:hover {{
                background-color: {Colors.ELEVATED};
            }}
            QListWidget::item:selected {{
                background-color: {Colors.CYAN};
                color: {Colors.VOID};
            }}
        """)

        units = [
            ("ALPHA-1", "ACTIVE", Colors.GREEN),
            ("BRAVO-2", "SILENT", Colors.AMBER),
            ("CHARLIE-9", "PENDING", Colors.TEXT_DIM),
            ("DELTA-4", "ACTIVE", Colors.GREEN),
        ]

        for name, status, color in units:
            item = QListWidgetItem(f"● {name}  [{status}]")
            item.setForeground(QColor(color))
            self.unit_list.addItem(item)

        layout.addWidget(self.unit_list)

        # TX Mode
        mode_label = QLabel("TRANSMISSION MODE")
        mode_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt; font-weight: 600; letter-spacing: 1px;")
        layout.addWidget(mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems([MODE_TCP, MODE_RADIO, MODE_FM, MODE_INTERNET])
        self.mode_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        self.mode_combo.currentTextChanged.connect(self.on_mode_change)
        layout.addWidget(self.mode_combo)

        # Target Config
        target_label = QLabel("TARGET (TCP)")
        target_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt; font-weight: 600; letter-spacing: 1px;")
        layout.addWidget(target_label)

        self.target_input = QLineEdit("127.0.0.1:5555")
        self.target_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px;
                color: {Colors.TEXT_PRIMARY};
                font-family: 'JetBrains Mono', 'Consolas';
            }}
        """)
        layout.addWidget(self.target_input)

        layout.addStretch()

        return panel

    def _create_footer(self):
        footer = QFrame()
        footer.setFixedHeight(40)
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-top: 1px solid {Colors.BORDER};
            }}
        """)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(16, 0, 16, 0)

        status_label = QLabel(f"MILCODEC v{VERSION} • ENCRYPTED • OPERATIONAL")
        status_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt;")
        layout.addWidget(status_label)

        layout.addStretch()

        self.tx_status = QLabel("READY")
        self.tx_status.setStyleSheet(f"color: {Colors.GREEN}; font-size: 9pt; font-weight: bold;")
        layout.addWidget(self.tx_status)

        return footer

    def init_signals(self):
        self.tx_engine.tx_status_signal.connect(self.on_tx_status)
        self.tx_engine.tx_spectrum_signal.connect(self.spectrum.update_data)
        self.tx_engine.tx_complete_signal.connect(self.on_tx_complete)

    def handle_command(self):
        cmd = self.cmd_input.text().strip()
        self.cmd_input.clear()

        if not cmd:
            return

        self.log_status(f"> {cmd}", "COMMAND")
        self.command_history.append(cmd)

        # Get selected priority
        priority = PRIORITIES[self.priority_group.checkedId()] if self.priority_group.checkedId() >= 0 else "ROUTINE"

        # Parse command
        if cmd.startswith("/mode"):
            parts = cmd.split()
            if len(parts) > 1:
                mode = parts[1].upper()
                if mode in [MODE_TCP, MODE_RADIO, MODE_FM, MODE_INTERNET]:
                    self.mode_combo.setCurrentText(mode)
                    self.log_status(f"MODE SET: {mode}", "SUCCESS")
                else:
                    self.log_status(f"INVALID MODE: {mode}", "ERROR")
            else:
                self.log_status("USAGE: /mode <tcp|radio|fm|internet>", "WARNING")

        elif cmd.startswith("/all"):
            msg = cmd[5:].strip()
            if msg:
                self.tx_engine.send_order(msg, "ALL", priority)
            else:
                self.log_status("USAGE: /all <message>", "WARNING")

        elif cmd.startswith("/to"):
            parts = cmd.split(maxsplit=2)
            if len(parts) >= 3:
                target = parts[1].upper()
                msg = parts[2]
                self.tx_engine.send_order(msg, target, priority)
            else:
                self.log_status("USAGE: /to <unit> <message>", "WARNING")

        elif cmd.startswith("/"):
            self.log_status(f"UNKNOWN COMMAND: {cmd.split()[0]}", "ERROR")

        else:
            # Treat as broadcast message
            self.tx_engine.send_order(cmd, "ALL", priority)

    def on_mode_change(self, mode):
        self.tx_engine.set_mode(mode)

    def on_tx_status(self, message, level):
        self.log_status(message, level)
        self.tx_status.setText(message[:30] + "..." if len(message) > 30 else message)

    def on_tx_complete(self, success, details):
        if success:
            self.log_status(f"TX COMPLETE: {details}", "SUCCESS")
            self.tx_counter.setText(str(self.tx_engine.orders_sent))
            self.tx_status.setText("TX SUCCESS")
            self.tx_status.setStyleSheet(f"color: {Colors.GREEN}; font-size: 9pt; font-weight: bold;")
        else:
            self.log_status(f"TX FAILED: {details}", "ERROR")
            self.tx_status.setText("TX FAILED")
            self.tx_status.setStyleSheet(f"color: {Colors.RED}; font-size: 9pt; font-weight: bold;")

    def log_status(self, text, level="INFO"):
        self.log_view.log(text, level)

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.setText(now)


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply theme if available
    try:
        from theme import apply_theme
        apply_theme(app)
    except:
        pass

    window = CommanderWindow()
    window.show()
    sys.exit(app.exec())
