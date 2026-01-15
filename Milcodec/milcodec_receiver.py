"""
MILCODEC RECEIVER TERMINAL v2.0 - "NIGHT WATCH"
================================================
Professional field unit for secure signal reception and decryption.
Features Palantir-inspired UI with real-time signal visualization.
"""

import sys
import os
import time
import socket
import threading
import queue
import numpy as np
import collections
import random
from datetime import datetime

# GUI Imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLabel, QProgressBar, QPushButton, QFrame, QSizePolicy,
    QGroupBox, QStackedWidget, QComboBox, QSplitter, QScrollArea,
    QSpacerItem, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QMutex, QPropertyAnimation,
    QEasingCurve, QSize
)
from PyQt6.QtGui import (
    QColor, QPalette, QFont, QPainter, QPen, QBrush, QLinearGradient,
    QRadialGradient, QPainterPath
)

# Cryptography Imports
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# Theme Import
try:
    from theme import Colors, Fonts, Styles, apply_theme, create_glow_effect, StatusColors
except ImportError:
    # Fallback colors if theme not found
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
# CONSTANTS & PROTOCOLS
# =============================================================================
VERSION = "2.0.0"
SAMPLE_RATE = 44100
BUFFER_SIZE = 1024
RX_BUFFER_MAX = 44100 * 10
PNC_KEY = np.array([
    1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,
    0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0
], dtype=np.float32) * 2 - 1

# Message Priority Levels
PRIORITY_FLASH = "FLASH"
PRIORITY_IMMEDIATE = "IMMEDIATE"
PRIORITY_PRIORITY = "PRIORITY"
PRIORITY_ROUTINE = "ROUTINE"

PRIORITY_COLORS = {
    PRIORITY_FLASH: Colors.RED,
    PRIORITY_IMMEDIATE: Colors.AMBER,
    PRIORITY_PRIORITY: Colors.CYAN,
    PRIORITY_ROUTINE: Colors.TEXT_SECONDARY
}

# =============================================================================
# CRYPTOGRAPHY ENGINE ("THE SHIELD")
# =============================================================================
class CryptoEngine:
    """
    Post-Quantum Cryptography Engine.
    Simulates CRYSTALS-Kyber KEM + ChaCha20-Poly1305 encryption.
    """
    def __init__(self):
        self.private_key = b"TOP_SECRET_BURN_ON_CAPTURE_KEY32"
        self.public_key_commander = b"COMMANDER_PUBLIC_KEY_V2_32BYTES"
        self.session_key = None
        self.is_burned = False
        self.messages_decrypted = 0

    def decrypt_payload(self, encrypted_blob):
        """
        Decapsulate and decrypt incoming payload.
        Returns: (plaintext, status, priority)
        """
        if self.is_burned:
            return None, "KEYS BURNED - CANNOT DECRYPT", PRIORITY_ROUTINE

        # Simulated Kyber decapsulation
        shared_secret = b"KyberSharedSecret_Simulated_32B"

        if not CRYPTO_AVAILABLE:
            return encrypted_blob.decode('utf-8', errors='ignore'), "CRYPTO UNAVAILABLE", PRIORITY_ROUTINE

        try:
            text = encrypted_blob.decode('utf-8')
            # Parse command format: CMD:[TARGET]:[PRIORITY]:[MESSAGE]
            if text.startswith("CMD:"):
                parts = text.split(":", 3)
                if len(parts) >= 4:
                    target = parts[1]
                    priority = parts[2] if parts[2] in PRIORITY_COLORS else PRIORITY_ROUTINE
                    message = parts[3]
                    self.messages_decrypted += 1
                    return message, "VERIFIED", priority
                else:
                    self.messages_decrypted += 1
                    return text[4:], "VERIFIED", PRIORITY_ROUTINE
            return None, "INVALID FORMAT", PRIORITY_ROUTINE
        except Exception as e:
            return None, f"DECRYPT ERROR: {str(e)}", PRIORITY_ROUTINE

    def verify_signature(self, message, signature):
        """Verify Commander's digital signature (simulated)."""
        return not self.is_burned

    def burn_keys(self):
        """Secure memory wipe - Protocol Zero."""
        self.private_key = b"\x00" * 32
        self.session_key = None
        self.is_burned = True
        return True

    def get_status(self):
        if self.is_burned:
            return "BURNED"
        return "OPERATIONAL"

# =============================================================================
# SIGNAL PROCESSOR ("THE EAR")
# =============================================================================
class SignalProcessor(QThread):
    sig_feed_update = pyqtSignal(str, str)  # message, priority
    sig_snr_update = pyqtSignal(float)
    sig_waveform_update = pyqtSignal(list)
    sig_status_update = pyqtSignal(str, str)  # status, level
    sig_stats_update = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.is_running = True
        self.mutex = QMutex()
        self.data_queue = queue.Queue()
        self.crypto = CryptoEngine()
        self.source_mode = "SIMULATION"  # SIMULATION, MICROPHONE, FILE, NETWORK
        
        # Statistics
        self.packets_received = 0
        self.packets_decoded = 0
        self.start_time = time.time()

    def run(self):
        self.sig_status_update.emit("INITIALIZING SENSOR ARRAY...", "PENDING")
        threading.Thread(target=self._audio_stream_loop, daemon=True).start()
        self._processor_loop()

    def _audio_stream_loop(self):
        """Audio input with multiple source support."""
        if self.source_mode == "MICROPHONE":
            try:
                import pyaudio
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE,
                    input=True, frames_per_buffer=BUFFER_SIZE
                )
                self.sig_status_update.emit("AUDIO: HARDWARE ACTIVE", "CONNECTED")
                while self.is_running:
                    data = stream.read(BUFFER_SIZE, exception_on_overflow=False)
                    fdata = np.frombuffer(data, dtype=np.float32)
                    self.data_queue.put(fdata)
            except Exception as e:
                self.sig_status_update.emit(f"AUDIO FAILED: {str(e)}", "ERROR")
                self._run_simulation()
        else:
            self._run_simulation()

    def _run_simulation(self):
        """Generate simulated signal data with periodic messages."""
        self.sig_status_update.emit("SIMULATION MODE ACTIVE", "CONNECTED")
        t = 0
        last_msg_time = time.time()
        msg_index = 0
        
        test_messages = [
            ("CMD:ALL:FLASH:HOSTILE CONTACT DETECTED SECTOR 7", PRIORITY_FLASH),
            ("CMD:ALPHA:IMMEDIATE:EXTRACT AT CHECKPOINT BRAVO 0300Z", PRIORITY_IMMEDIATE),
            ("CMD:ALL:PRIORITY:MAINTAIN RADIO SILENCE UNTIL FURTHER NOTICE", PRIORITY_PRIORITY),
            ("CMD:ALL:ROUTINE:SUPPLY DROP CONFIRMED GRID REF 45N12E", PRIORITY_ROUTINE),
        ]

        while self.is_running:
            # Generate noise floor
            noise = np.random.normal(0, 0.05, BUFFER_SIZE).astype(np.float32)

            # Inject message every 6 seconds
            if time.time() - last_msg_time > 6:
                t_vec = np.linspace(t, t + BUFFER_SIZE/SAMPLE_RATE, BUFFER_SIZE)
                carrier = 0.8 * np.sin(2 * np.pi * 440 * t_vec)
                noise += carrier.astype(np.float32)

                if time.time() - last_msg_time > 6.3:
                    last_msg_time = time.time()
                    msg, priority = test_messages[msg_index % len(test_messages)]
                    self.data_queue.put(("MSG_TRIGGER", msg))
                    msg_index += 1

            if self.is_running:
                self.data_queue.put(noise)

            t += BUFFER_SIZE / SAMPLE_RATE
            time.sleep(BUFFER_SIZE / SAMPLE_RATE)

    def _processor_loop(self):
        """Main signal processing loop with DSSS correlation."""
        while self.is_running:
            try:
                chunk = self.data_queue.get(timeout=1)

                # Handle message triggers from simulation
                if isinstance(chunk, tuple) and chunk[0] == "MSG_TRIGGER":
                    self.packets_received += 1
                    self._handle_decoded_message(chunk[1])
                    continue

                if not isinstance(chunk, np.ndarray):
                    continue

                # DSP Analysis
                rms = np.sqrt(np.mean(chunk ** 2))
                snr = max(0, min(100, (20 * np.log10(rms + 1e-9) + 60) * 1.5))
                self.sig_snr_update.emit(snr)

                # Waveform for visualization
                downsampled = chunk[::4].tolist()[:64]
                self.sig_waveform_update.emit(downsampled)

                # Real DSSS correlation would go here
                # correlation = np.correlate(chunk, PNC_KEY, 'valid')
                # if np.max(correlation) > threshold: extract_bits()

            except queue.Empty:
                pass

        self._emit_stats()

    def _handle_decoded_message(self, encrypted_content):
        """Process decoded message through crypto engine."""
        decrypted, status, priority = self.crypto.decrypt_payload(encrypted_content.encode('utf-8'))

        timestamp = datetime.now().strftime("%H:%M:%Sz")
        if decrypted:
            self.packets_decoded += 1
            log_entry = f"[{timestamp}] {decrypted}"
            self.sig_feed_update.emit(log_entry, priority)
        else:
            self.sig_feed_update.emit(f"[{timestamp}] DECODE FAILED: {status}", "ERROR")

        self._emit_stats()

    def _emit_stats(self):
        """Emit current statistics."""
        uptime = int(time.time() - self.start_time)
        stats = {
            'packets_received': self.packets_received,
            'packets_decoded': self.packets_decoded,
            'crypto_status': self.crypto.get_status(),
            'uptime': uptime,
            'messages_decrypted': self.crypto.messages_decrypted
        }
        self.sig_stats_update.emit(stats)

    def burn(self):
        """Execute Protocol Zero."""
        self.crypto.burn_keys()
        self.sig_status_update.emit("PROTOCOL ZERO EXECUTED", "ERROR")

    def stop(self):
        self.is_running = False

# =============================================================================
# CUSTOM WIDGETS
# =============================================================================
class SNRGraph(QFrame):
    """Advanced SNR visualization with gradient fill and grid."""
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(120)
        self.history = collections.deque([0] * 150, maxlen=150)
        self.setStyleSheet(f"background: transparent; border: none;")

    def update_val(self, val):
        self.history.append(val)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()

        # Background
        painter.fillRect(0, 0, w, h, QColor(Colors.VOID))

        # Grid
        painter.setPen(QPen(QColor(Colors.BORDER_DIM), 1, Qt.PenStyle.DotLine))
        for x in range(0, w, 30):
            painter.drawLine(x, 0, x, h)
        for y in range(0, h, 20):
            painter.drawLine(0, y, w, y)

        # SNR threshold line at 50%
        painter.setPen(QPen(QColor(Colors.AMBER), 1, Qt.PenStyle.DashLine))
        mid_y = h // 2
        painter.drawLine(0, mid_y, w, mid_y)

        # Build path
        if len(self.history) < 2:
            return

        path = QPainterPath()
        step = w / (len(self.history) - 1)

        points = []
        for i, val in enumerate(self.history):
            x = i * step
            y = h - (val / 100.0 * h)
            points.append((x, y))

        # Start path for fill
        path.moveTo(0, h)
        for x, y in points:
            path.lineTo(x, y)
        path.lineTo(w, h)
        path.closeSubpath()

        # Gradient fill
        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0, QColor(0, 212, 255, 80))
        gradient.setColorAt(1, QColor(0, 212, 255, 10))
        painter.fillPath(path, gradient)

        # Signal line with glow
        painter.setPen(QPen(QColor(Colors.CYAN), 2))
        for i in range(len(points) - 1):
            painter.drawLine(
                int(points[i][0]), int(points[i][1]),
                int(points[i + 1][0]), int(points[i + 1][1])
            )

        # Current value indicator
        if points:
            last_x, last_y = points[-1]
            painter.setBrush(QBrush(QColor(Colors.CYAN)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(last_x) - 4, int(last_y) - 4, 8, 8)


class WaveformDisplay(QFrame):
    """Real-time waveform oscilloscope display."""
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(80)
        self.data = []
        self.setStyleSheet("background: transparent;")

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        mid_y = h // 2

        # Background
        painter.fillRect(0, 0, w, h, QColor(Colors.VOID))

        # Center line
        painter.setPen(QPen(QColor(Colors.BORDER_DIM), 1))
        painter.drawLine(0, mid_y, w, mid_y)

        if not self.data:
            return

        # Waveform
        painter.setPen(QPen(QColor(Colors.GREEN), 1))
        step = w / len(self.data)

        for i in range(len(self.data) - 1):
            x1 = int(i * step)
            y1 = int(mid_y - self.data[i] * mid_y * 10)
            x2 = int((i + 1) * step)
            y2 = int(mid_y - self.data[i + 1] * mid_y * 10)
            painter.drawLine(x1, y1, x2, y2)


class StatusIndicator(QFrame):
    """Animated status dot indicator."""
    def __init__(self, size=10):
        super().__init__()
        self.setFixedSize(size, size)
        self.status = "OFFLINE"
        self._pulse = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate)
        self.timer.start(50)

    def set_status(self, status):
        self.status = status
        self.update()

    def _animate(self):
        self._pulse = (self._pulse + 5) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color_map = {
            'CONNECTED': Colors.GREEN,
            'PENDING': Colors.AMBER,
            'ERROR': Colors.RED,
            'OFFLINE': Colors.TEXT_DIM,
        }
        color = QColor(color_map.get(self.status, Colors.TEXT_DIM))

        # Pulse effect for active states
        if self.status in ['CONNECTED', 'PENDING']:
            import math
            alpha = int(128 + 127 * math.sin(math.radians(self._pulse)))
            color.setAlpha(alpha)

        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(1, 1, self.width() - 2, self.height() - 2)


class MessageFeed(QTextEdit):
    """Enhanced message feed with priority-based coloring."""
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
                color: {Colors.TEXT_PRIMARY};
            }}
        """)

    def add_message(self, text, priority=PRIORITY_ROUTINE):
        color = PRIORITY_COLORS.get(priority, Colors.TEXT_SECONDARY)
        prefix = ""
        if priority == PRIORITY_FLASH:
            prefix = "⚠ FLASH ▶ "
        elif priority == PRIORITY_IMMEDIATE:
            prefix = "◆ IMMED ▶ "
        elif priority == PRIORITY_PRIORITY:
            prefix = "● PRIOR ▶ "
        else:
            prefix = "○ ROUT  ▶ "

        self.append(f'<span style="color: {color};">{prefix}{text}</span>')
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


# =============================================================================
# MAIN WINDOW ("THE NIGHT WATCH")
# =============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.processor = SignalProcessor()
        self.init_ui()
        self.init_signals()
        self.processor.start()

    def init_ui(self):
        self.setWindowTitle(f"MILCODEC RECEIVER v{VERSION} - NIGHT WATCH")
        self.setGeometry(100, 100, 900, 750)
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

        # === CONTENT AREA ===
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(16, 16, 16, 16)

        # Row 1: Status Cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(12)

        self.card_crypto = self._create_stat_card("CRYPTO STATUS", "OPERATIONAL", Colors.GREEN)
        self.card_packets = self._create_stat_card("PACKETS RX", "0", Colors.CYAN)
        self.card_decoded = self._create_stat_card("DECODED", "0", Colors.CYAN)
        self.card_uptime = self._create_stat_card("UPTIME", "0s", Colors.TEXT_SECONDARY)

        cards_row.addWidget(self.card_crypto)
        cards_row.addWidget(self.card_packets)
        cards_row.addWidget(self.card_decoded)
        cards_row.addWidget(self.card_uptime)
        content_layout.addLayout(cards_row)

        # Row 2: Signal Analysis
        signal_panel = self._create_panel("SIGNAL INTEGRITY MONITOR")
        signal_layout = QVBoxLayout()
        signal_layout.setSpacing(8)

        self.snr_graph = SNRGraph()
        signal_layout.addWidget(self.snr_graph)

        wave_row = QHBoxLayout()
        wave_label = QLabel("WAVEFORM")
        wave_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt;")
        wave_row.addWidget(wave_label)
        wave_row.addStretch()
        signal_layout.addLayout(wave_row)

        self.waveform = WaveformDisplay()
        signal_layout.addWidget(self.waveform)

        signal_panel.layout().addLayout(signal_layout)
        content_layout.addWidget(signal_panel)

        # Row 3: Intelligence Feed
        feed_panel = self._create_panel("DECRYPTED INTELLIGENCE FEED")
        self.message_feed = MessageFeed()
        feed_panel.layout().addWidget(self.message_feed)
        content_layout.addWidget(feed_panel, stretch=1)

        main_layout.addWidget(content, stretch=1)

        # === FOOTER / CONTROLS ===
        footer = self._create_footer()
        main_layout.addWidget(footer)

        # Clock timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

    def _create_header(self):
        header = QFrame()
        header.setObjectName("Header")
        header.setFixedHeight(60)
        header.setStyleSheet(f"""
            QFrame#Header {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {Colors.ELEVATED}, stop:1 {Colors.SURFACE});
                border-bottom: 1px solid {Colors.BORDER};
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 0, 16, 0)

        # Left: Title
        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        title = QLabel("MILCODEC RECEIVER")
        title.setStyleSheet(f"""
            font-size: 14pt;
            font-weight: 600;
            color: {Colors.CYAN};
            letter-spacing: 2px;
        """)

        subtitle = QLabel("NIGHT WATCH TERMINAL • SECURE FIELD UNIT")
        subtitle.setStyleSheet(f"font-size: 9pt; color: {Colors.TEXT_DIM};")

        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        layout.addLayout(title_col)

        layout.addStretch()

        # Center: Status
        status_col = QHBoxLayout()
        status_col.setSpacing(8)

        self.status_indicator = StatusIndicator()
        self.status_label = QLabel("INITIALIZING...")
        self.status_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 10pt;")

        status_col.addWidget(self.status_indicator)
        status_col.addWidget(self.status_label)
        layout.addLayout(status_col)

        layout.addStretch()

        # Right: Clock
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet(f"""
            font-family: 'JetBrains Mono', 'Consolas';
            font-size: 12pt;
            color: {Colors.AMBER};
        """)
        layout.addWidget(self.clock_label)

        return header

    def _create_panel(self, title):
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
        layout.setSpacing(8)

        label = QLabel(title)
        label.setStyleSheet(f"""
            color: {Colors.TEXT_DIM};
            font-size: 9pt;
            font-weight: 600;
            letter-spacing: 1px;
        """)
        layout.addWidget(label)

        return panel

    def _create_stat_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 6px;
                padding: 8px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(4)
        layout.setContentsMargins(12, 8, 12, 8)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 8pt; letter-spacing: 1px;")

        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet(f"color: {color}; font-size: 16pt; font-weight: bold;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card

    def _create_footer(self):
        footer = QFrame()
        footer.setFixedHeight(60)
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-top: 1px solid {Colors.BORDER};
            }}
        """)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(16, 0, 16, 0)

        # Source selector
        source_label = QLabel("INPUT SOURCE:")
        source_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 9pt;")
        layout.addWidget(source_label)

        self.source_combo = QComboBox()
        self.source_combo.addItems(["SIMULATION", "MICROPHONE", "NETWORK", "FILE"])
        self.source_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 6px 12px;
                color: {Colors.TEXT_PRIMARY};
                min-width: 120px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(self.source_combo)

        layout.addStretch()

        # Panic button
        self.btn_panic = QPushButton("◉  PROTOCOL ZERO  ◉")
        self.btn_panic.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_panic.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a1a1a, stop:1 #1a0a0a);
                border: 2px solid {Colors.RED};
                border-radius: 4px;
                padding: 10px 24px;
                color: {Colors.RED};
                font-weight: bold;
                font-size: 11pt;
                letter-spacing: 2px;
            }}
            QPushButton:hover {{
                background-color: {Colors.RED};
                color: {Colors.VOID};
            }}
        """)
        self.btn_panic.clicked.connect(self.panic_wipe)
        layout.addWidget(self.btn_panic)

        return footer

    def init_signals(self):
        self.processor.sig_feed_update.connect(self.add_feed_message)
        self.processor.sig_snr_update.connect(self.snr_graph.update_val)
        self.processor.sig_waveform_update.connect(self.waveform.set_data)
        self.processor.sig_status_update.connect(self.update_status)
        self.processor.sig_stats_update.connect(self.update_stats)

    def add_feed_message(self, text, priority):
        self.message_feed.add_message(text, priority)

    def update_status(self, status, level):
        self.status_label.setText(status)
        self.status_indicator.set_status(level)
        
        color = {
            'CONNECTED': Colors.GREEN,
            'PENDING': Colors.AMBER,
            'ERROR': Colors.RED,
        }.get(level, Colors.TEXT_SECONDARY)
        
        self.status_label.setStyleSheet(f"color: {color}; font-size: 10pt;")

    def update_stats(self, stats):
        self.card_packets.findChild(QLabel, "value").setText(str(stats['packets_received']))
        self.card_decoded.findChild(QLabel, "value").setText(str(stats['packets_decoded']))
        self.card_uptime.findChild(QLabel, "value").setText(f"{stats['uptime']}s")
        
        crypto_color = Colors.GREEN if stats['crypto_status'] == 'OPERATIONAL' else Colors.RED
        crypto_label = self.card_crypto.findChild(QLabel, "value")
        crypto_label.setText(stats['crypto_status'])
        crypto_label.setStyleSheet(f"color: {crypto_color}; font-size: 16pt; font-weight: bold;")

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.setText(now)

    def panic_wipe(self):
        self.processor.burn()
        self.btn_panic.setText("WIPING...")
        self.btn_panic.setEnabled(False)
        self.message_feed.add_message("INITIATING CRYPTOGRAPHIC PURGE...", PRIORITY_FLASH)
        self.message_feed.add_message("ALL KEYS DESTROYED", PRIORITY_FLASH)
        self.message_feed.add_message("SYSTEM CLEAN - CLOSING IN 3 SECONDS", PRIORITY_FLASH)
        QTimer.singleShot(3000, self.close)

    def closeEvent(self, event):
        self.processor.stop()
        self.processor.wait()
        super().closeEvent(event)


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

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
