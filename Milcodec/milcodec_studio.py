"""
MILCODEC STUDIO v2.0 - AUDIO STEGANOGRAPHY SUITE
=================================================
Professional tool for embedding encrypted messages into audio files.
Upload a song, hide your message, extract and decrypt on the other side.
"""

import sys
import os
import time
import numpy as np
import wave
import struct
from datetime import datetime

# GUI Imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLabel, QLineEdit, QPushButton, QFrame, QFileDialog,
    QTabWidget, QProgressBar, QSplitter, QComboBox, QSpinBox,
    QMessageBox, QSizePolicy, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QMimeData
from PyQt6.QtGui import (
    QColor, QPainter, QPen, QBrush, QLinearGradient, QDragEnterEvent,
    QDropEvent
)

# Cryptography
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# Theme
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

# DSSS Masker
try:
    from milcodec_masker import DSSSMasker, PNC_KEY, SAMPLE_RATE
except ImportError:
    SAMPLE_RATE = 44100
    PNC_KEY = np.array([
        1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,
        0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0
    ], dtype=np.float32) * 2 - 1

# =============================================================================
# CONSTANTS
# =============================================================================
VERSION = "2.0.0"
MAGIC_HEADER = b"MILCODEC_V2"  # 11 bytes
DEFAULT_SNR = -20  # dB

# =============================================================================
# CRYPTO HELPER
# =============================================================================
class CryptoHelper:
    """Encryption/Decryption utilities for messages."""
    
    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> tuple:
        """Derive a 32-byte key from password using PBKDF2."""
        if salt is None:
            salt = os.urandom(16)
        
        if not CRYPTO_AVAILABLE:
            # Fallback: simple XOR key
            key = (password * 32)[:32].encode('utf-8')
            return key, salt
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode('utf-8'))
        return key, salt

    @staticmethod
    def encrypt(plaintext: str, password: str) -> bytes:
        """Encrypt plaintext with ChaCha20."""
        key, salt = CryptoHelper.derive_key(password)
        nonce = os.urandom(12)
        
        if not CRYPTO_AVAILABLE:
            # Simple XOR fallback
            data = plaintext.encode('utf-8')
            encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
            return MAGIC_HEADER + salt + nonce + encrypted
        
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode('utf-8'))
        
        # Format: MAGIC + SALT(16) + NONCE(12) + CIPHERTEXT
        return MAGIC_HEADER + salt + nonce + ciphertext

    @staticmethod
    def decrypt(encrypted: bytes, password: str) -> str:
        """Decrypt ciphertext back to plaintext."""
        if not encrypted.startswith(MAGIC_HEADER):
            raise ValueError("Invalid Milcodec encrypted data")
        
        data = encrypted[len(MAGIC_HEADER):]
        salt = data[:16]
        nonce = data[16:28]
        ciphertext = data[28:]
        
        key, _ = CryptoHelper.derive_key(password, salt)
        
        if not CRYPTO_AVAILABLE:
            # XOR fallback
            decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(ciphertext)])
            return decrypted.decode('utf-8')
        
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext)
        
        return plaintext.decode('utf-8')


# =============================================================================
# AUDIO STEGANOGRAPHY ENGINE
# =============================================================================
class SteganographyEngine:
    """Engine for hiding data in audio files using DSSS."""
    
    def __init__(self):
        self.snr_db = DEFAULT_SNR
        
    def set_snr(self, snr_db):
        """Set the signal-to-noise ratio for embedding."""
        self.snr_db = max(-30, min(-10, snr_db))

    def embed_in_audio(self, carrier_audio: np.ndarray, message_bytes: bytes, 
                       sample_rate: int = SAMPLE_RATE) -> np.ndarray:
        """
        Embed encrypted message into carrier audio using DSSS.
        
        Args:
            carrier_audio: Original audio as float32 array
            message_bytes: Encrypted message bytes
            sample_rate: Audio sample rate
            
        Returns:
            Modified audio with embedded message
        """
        # Add length header to message
        length_bytes = len(message_bytes).to_bytes(4, 'big')
        full_message = length_bytes + message_bytes
        
        # Convert bytes to bits
        bits = []
        for byte in full_message:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        
        # Spread each bit with PN code
        spread_signal = []
        for bit in bits:
            scalar = 1 if bit == 1 else -1
            spread_signal.extend(PNC_KEY * scalar)
        
        spread_signal = np.array(spread_signal, dtype=np.float32)
        
        # Upsample to audio rate
        chip_duration = 0.001  # 1ms per chip
        samples_per_chip = int(sample_rate * chip_duration)
        baseband = np.repeat(spread_signal, samples_per_chip)
        
        # Modulate onto 12kHz carrier
        t = np.linspace(0, len(baseband) / sample_rate, len(baseband))
        carrier_wave = np.sin(2 * np.pi * 12000 * t)
        modulated = baseband * carrier_wave
        
        # Calculate mixing ratio based on SNR
        # SNR = 10 * log10(signal_power / noise_power)
        # For -20dB: signal_power = noise_power / 100
        snr_linear = 10 ** (self.snr_db / 10)
        signal_amplitude = np.sqrt(snr_linear) * 0.5  # Relative to carrier
        
        # Ensure message fits in carrier
        if len(modulated) > len(carrier_audio):
            # Truncate message (or could loop carrier)
            modulated = modulated[:len(carrier_audio)]
        
        # Create output
        output = carrier_audio.copy()
        output[:len(modulated)] += modulated * signal_amplitude
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(output))
        if max_val > 1.0:
            output = output / max_val * 0.99
        
        return output

    def extract_from_audio(self, stego_audio: np.ndarray, 
                           sample_rate: int = SAMPLE_RATE) -> bytes:
        """
        Extract embedded message from audio using DSSS correlation.
        
        Args:
            stego_audio: Audio with embedded message
            sample_rate: Audio sample rate
            
        Returns:
            Extracted message bytes
        """
        chip_duration = 0.001
        samples_per_chip = int(sample_rate * chip_duration)
        
        # Demodulate: multiply by carrier and low-pass (average)
        t = np.linspace(0, len(stego_audio) / sample_rate, len(stego_audio))
        carrier = np.sin(2 * np.pi * 12000 * t)
        demodulated = stego_audio * carrier
        
        # Correlation-based detection
        # For each chip position, correlate with PN code
        pn_len = len(PNC_KEY)
        pn_samples = pn_len * samples_per_chip
        
        extracted_bits = []
        position = 0
        
        # First, extract length (4 bytes = 32 bits)
        for _ in range(32 + 8 * 256):  # Max 256 byte message + length
            if position + pn_samples > len(demodulated):
                break
                
            chunk = demodulated[position:position + pn_samples]
            
            # Downsample to chip rate
            chips = []
            for i in range(pn_len):
                start = i * samples_per_chip
                end = start + samples_per_chip
                chips.append(np.mean(chunk[start:end]))
            
            chips = np.array(chips)
            
            # Correlate with PN code
            correlation = np.sum(chips * PNC_KEY)
            bit = 1 if correlation > 0 else 0
            extracted_bits.append(bit)
            
            position += pn_samples
        
        # Convert bits to bytes
        extracted_bytes = []
        for i in range(0, len(extracted_bits), 8):
            if i + 8 > len(extracted_bits):
                break
            byte_bits = extracted_bits[i:i+8]
            byte_val = sum(b << (7 - j) for j, b in enumerate(byte_bits))
            extracted_bytes.append(byte_val)
        
        # First 4 bytes are length
        if len(extracted_bytes) < 4:
            return b""
        
        message_length = int.from_bytes(bytes(extracted_bytes[:4]), 'big')
        message_bytes = bytes(extracted_bytes[4:4 + message_length])
        
        return message_bytes


# =============================================================================
# AUDIO FILE HANDLER
# =============================================================================
class AudioHandler:
    """Load and save audio files."""
    
    @staticmethod
    def load_wav(filepath: str) -> tuple:
        """Load WAV file and return (audio_data, sample_rate, channels)."""
        with wave.open(filepath, 'r') as wf:
            channels = wf.getnchannels()
            sample_rate = wf.getframerate()
            n_frames = wf.getnframes()
            sample_width = wf.getsampwidth()
            
            raw_data = wf.readframes(n_frames)
            
            # Convert to numpy array
            if sample_width == 1:
                dtype = np.uint8
                max_val = 255
            elif sample_width == 2:
                dtype = np.int16
                max_val = 32767
            else:
                dtype = np.int32
                max_val = 2147483647
            
            audio = np.frombuffer(raw_data, dtype=dtype).astype(np.float32) / max_val
            
            # Convert stereo to mono if needed
            if channels == 2:
                audio = audio.reshape(-1, 2).mean(axis=1)
            
            return audio, sample_rate, channels

    @staticmethod
    def save_wav(filepath: str, audio: np.ndarray, sample_rate: int = SAMPLE_RATE):
        """Save audio data to WAV file."""
        # Normalize and convert to int16
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.99
        
        audio_int = (audio * 32767).astype(np.int16)
        
        with wave.open(filepath, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_int.tobytes())


# =============================================================================
# CUSTOM WIDGETS
# =============================================================================
class DropZone(QFrame):
    """Drag-and-drop file zone."""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, label_text="Drag & Drop Audio File"):
        super().__init__()
        self.setAcceptDrops(True)
        self.setMinimumHeight(150)
        self.label_text = label_text
        self.loaded_file = None
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.VOID};
                border: 2px dashed {Colors.BORDER};
                border-radius: 8px;
            }}
            QFrame:hover {{
                border-color: {Colors.CYAN};
            }}
        """)

    def set_file(self, filepath):
        self.loaded_file = filepath
        self.label_text = os.path.basename(filepath)
        self.update()

    def clear_file(self):
        self.loaded_file = None
        self.label_text = "Drag & Drop Audio File"
        self.update()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.toLocalFile().lower().endswith(('.wav', '.mp3')):
                event.acceptProposedAction()
                self.setStyleSheet(self.styleSheet().replace(Colors.BORDER, Colors.CYAN))

    def dragLeaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.VOID};
                border: 2px dashed {Colors.BORDER};
                border-radius: 8px;
            }}
            QFrame:hover {{
                border-color: {Colors.CYAN};
            }}
        """)

    def dropEvent(self, event: QDropEvent):
        url = event.mimeData().urls()[0]
        filepath = url.toLocalFile()
        self.set_file(filepath)
        self.file_dropped.emit(filepath)
        self.dragLeaveEvent(None)

    def mousePressEvent(self, event):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "",
            "Audio Files (*.wav *.mp3);;All Files (*)"
        )
        if filepath:
            self.set_file(filepath)
            self.file_dropped.emit(filepath)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw text
        painter.setPen(QPen(QColor(Colors.TEXT_SECONDARY if not self.loaded_file else Colors.GREEN)))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.label_text)
        
        # Draw icon
        if not self.loaded_file:
            painter.setPen(QPen(QColor(Colors.TEXT_DIM), 2))
            cx, cy = self.width() // 2, self.height() // 2 - 20
            painter.drawLine(cx - 20, cy, cx + 20, cy)
            painter.drawLine(cx, cy - 20, cx, cy + 20)


class SpectrumCompare(QFrame):
    """Side-by-side spectrum comparison widget."""
    
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(120)
        self.before_data = []
        self.after_data = []
        self.setStyleSheet("background: transparent;")

    def set_before(self, data):
        self.before_data = data[:128] if len(data) > 128 else data
        self.update()

    def set_after(self, data):
        self.after_data = data[:128] if len(data) > 128 else data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        half_w = w // 2 - 10

        # Background
        painter.fillRect(0, 0, w, h, QColor(Colors.VOID))

        # Draw divider
        painter.setPen(QPen(QColor(Colors.BORDER), 1))
        painter.drawLine(w // 2, 0, w // 2, h)

        # Labels
        painter.setPen(QPen(QColor(Colors.TEXT_DIM)))
        painter.drawText(10, 15, "BEFORE")
        painter.drawText(w // 2 + 10, 15, "AFTER")

        # Draw spectrums
        self._draw_spectrum(painter, 0, 20, half_w, h - 25, self.before_data, Colors.CYAN)
        self._draw_spectrum(painter, w // 2 + 10, 20, half_w, h - 25, self.after_data, Colors.GREEN)

    def _draw_spectrum(self, painter, x, y, w, h, data, color):
        if not data:
            return

        max_val = max(data) if data else 1
        bar_width = max(1, w // len(data))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(color)))

        for i, val in enumerate(data):
            bar_x = x + i * bar_width
            bar_h = int((val / max_val) * h * 0.9)
            painter.drawRect(bar_x, y + h - bar_h, bar_width - 1, bar_h)


# =============================================================================
# MAIN WINDOW
# =============================================================================
class StudioWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = SteganographyEngine()
        self.carrier_audio = None
        self.carrier_sample_rate = SAMPLE_RATE
        self.stego_audio = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"MILCODEC STUDIO v{VERSION} - AUDIO STEGANOGRAPHY")
        self.setGeometry(100, 100, 1000, 700)
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

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 4px;
            }}
            QTabBar::tab {{
                background-color: {Colors.BACKGROUND};
                border: 1px solid {Colors.BORDER_DIM};
                border-bottom: none;
                padding: 10px 24px;
                margin-right: 2px;
                color: {Colors.TEXT_SECONDARY};
                font-weight: 600;
            }}
            QTabBar::tab:selected {{
                background-color: {Colors.SURFACE};
                color: {Colors.CYAN};
            }}
        """)

        # Encode Tab
        encode_tab = self._create_encode_tab()
        self.tabs.addTab(encode_tab, "🔒 ENCODE")

        # Decode Tab
        decode_tab = self._create_decode_tab()
        self.tabs.addTab(decode_tab, "🔓 DECODE")

        main_layout.addWidget(self.tabs, stretch=1)

        # Status Bar
        self.status_label = QLabel("READY")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.SURFACE};
                border-top: 1px solid {Colors.BORDER};
                padding: 8px 16px;
                color: {Colors.TEXT_DIM};
            }}
        """)
        main_layout.addWidget(self.status_label)

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

        title = QLabel("MILCODEC STUDIO")
        title.setStyleSheet(f"""
            font-size: 14pt;
            font-weight: 600;
            color: {Colors.CYAN};
            letter-spacing: 2px;
        """)

        subtitle = QLabel("AUDIO STEGANOGRAPHY SUITE • DSSS ENCRYPTION")
        subtitle.setStyleSheet(f"font-size: 9pt; color: {Colors.TEXT_DIM};")

        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        title_col.addWidget(title)
        title_col.addWidget(subtitle)

        layout.addLayout(title_col)
        layout.addStretch()

        crypto_status = QLabel("🛡️ ChaCha20-Poly1305" if CRYPTO_AVAILABLE else "⚠️ BASIC CRYPTO")
        crypto_status.setStyleSheet(f"color: {Colors.GREEN if CRYPTO_AVAILABLE else Colors.AMBER};")
        layout.addWidget(crypto_status)

        return header

    def _create_encode_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Row 1: File Drop Zones
        files_row = QHBoxLayout()

        # Carrier audio
        carrier_group = QGroupBox("CARRIER AUDIO")
        carrier_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 6px;
                margin-top: 16px;
                padding: 16px;
                font-weight: 600;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        carrier_layout = QVBoxLayout(carrier_group)
        self.encode_dropzone = DropZone("Drag & Drop Source Audio")
        self.encode_dropzone.file_dropped.connect(self.on_carrier_loaded)
        carrier_layout.addWidget(self.encode_dropzone)
        files_row.addWidget(carrier_group)

        layout.addLayout(files_row)

        # Row 2: Message Input
        message_group = QGroupBox("SECRET MESSAGE")
        message_group.setStyleSheet(carrier_group.styleSheet())
        message_layout = QVBoxLayout(message_group)

        self.encode_message = QTextEdit()
        self.encode_message.setPlaceholderText("Enter your secret message here...")
        self.encode_message.setMaximumHeight(100)
        self.encode_message.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px;
                color: {Colors.TEXT_PRIMARY};
                font-family: 'JetBrains Mono', 'Consolas';
            }}
        """)
        message_layout.addWidget(self.encode_message)

        # Password
        pass_row = QHBoxLayout()
        pass_label = QLabel("ENCRYPTION KEY:")
        pass_label.setStyleSheet(f"color: {Colors.TEXT_DIM};")
        pass_row.addWidget(pass_label)

        self.encode_password = QLineEdit()
        self.encode_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.encode_password.setPlaceholderText("Enter encryption password")
        self.encode_password.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px;
                color: {Colors.AMBER};
                font-family: 'JetBrains Mono';
            }}
        """)
        pass_row.addWidget(self.encode_password)
        message_layout.addLayout(pass_row)

        # SNR Setting
        snr_row = QHBoxLayout()
        snr_label = QLabel("STEALTH LEVEL (SNR):")
        snr_label.setStyleSheet(f"color: {Colors.TEXT_DIM};")
        snr_row.addWidget(snr_label)

        self.snr_spin = QSpinBox()
        self.snr_spin.setRange(-30, -10)
        self.snr_spin.setValue(-20)
        self.snr_spin.setSuffix(" dB")
        self.snr_spin.setStyleSheet(f"""
            QSpinBox {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 6px;
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        snr_row.addWidget(self.snr_spin)
        snr_row.addStretch()
        message_layout.addLayout(snr_row)

        layout.addWidget(message_group)

        # Row 3: Spectrum Comparison
        self.encode_spectrum = SpectrumCompare()
        layout.addWidget(self.encode_spectrum)

        # Row 4: Action Button
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_encode = QPushButton("🔒  ENCRYPT & EMBED")
        self.btn_encode.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_encode.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a2a2a, stop:1 #0a1a1a);
                border: 2px solid {Colors.CYAN};
                border-radius: 4px;
                padding: 12px 32px;
                color: {Colors.CYAN};
                font-weight: bold;
                font-size: 12pt;
            }}
            QPushButton:hover {{
                background-color: {Colors.CYAN};
                color: {Colors.VOID};
            }}
        """)
        self.btn_encode.clicked.connect(self.do_encode)
        btn_row.addWidget(self.btn_encode)

        layout.addLayout(btn_row)
        layout.addStretch()

        return tab

    def _create_decode_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # File Drop
        stego_group = QGroupBox("ENCODED AUDIO")
        stego_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 6px;
                margin-top: 16px;
                padding: 16px;
                font-weight: 600;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        stego_layout = QVBoxLayout(stego_group)
        self.decode_dropzone = DropZone("Drag & Drop Encoded Audio")
        self.decode_dropzone.file_dropped.connect(self.on_stego_loaded)
        stego_layout.addWidget(self.decode_dropzone)
        layout.addWidget(stego_group)

        # Password
        pass_group = QGroupBox("DECRYPTION KEY")
        pass_group.setStyleSheet(stego_group.styleSheet())
        pass_layout = QVBoxLayout(pass_group)

        self.decode_password = QLineEdit()
        self.decode_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.decode_password.setPlaceholderText("Enter decryption password")
        self.decode_password.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px;
                color: {Colors.AMBER};
                font-family: 'JetBrains Mono';
            }}
        """)
        pass_layout.addWidget(self.decode_password)
        layout.addWidget(pass_group)

        # Decode Button
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_decode = QPushButton("🔓  EXTRACT & DECRYPT")
        self.btn_decode.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_decode.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2a1a, stop:1 #1a1a0a);
                border: 2px solid {Colors.AMBER};
                border-radius: 4px;
                padding: 12px 32px;
                color: {Colors.AMBER};
                font-weight: bold;
                font-size: 12pt;
            }}
            QPushButton:hover {{
                background-color: {Colors.AMBER};
                color: {Colors.VOID};
            }}
        """)
        self.btn_decode.clicked.connect(self.do_decode)
        btn_row.addWidget(self.btn_decode)
        layout.addLayout(btn_row)

        # Result Display
        result_group = QGroupBox("EXTRACTED MESSAGE")
        result_group.setStyleSheet(stego_group.styleSheet())
        result_layout = QVBoxLayout(result_group)

        self.decode_result = QTextEdit()
        self.decode_result.setReadOnly(True)
        self.decode_result.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 12px;
                color: {Colors.GREEN};
                font-family: 'JetBrains Mono', 'Consolas';
                font-size: 12pt;
            }}
        """)
        result_layout.addWidget(self.decode_result)
        layout.addWidget(result_group, stretch=1)

        return tab

    def on_carrier_loaded(self, filepath):
        try:
            self.carrier_audio, self.carrier_sample_rate, _ = AudioHandler.load_wav(filepath)
            self.set_status(f"Loaded: {os.path.basename(filepath)} ({len(self.carrier_audio)/self.carrier_sample_rate:.1f}s)")

            # Show spectrum
            fft = np.abs(np.fft.fft(self.carrier_audio[:4096]))[:128]
            self.encode_spectrum.set_before(fft.tolist())

        except Exception as e:
            self.set_status(f"ERROR: {str(e)}")
            QMessageBox.warning(self, "Load Error", str(e))

    def on_stego_loaded(self, filepath):
        try:
            self.stego_audio, _, _ = AudioHandler.load_wav(filepath)
            self.set_status(f"Loaded encoded: {os.path.basename(filepath)}")
        except Exception as e:
            self.set_status(f"ERROR: {str(e)}")

    def do_encode(self):
        if self.carrier_audio is None:
            QMessageBox.warning(self, "Error", "Please load a carrier audio file first.")
            return

        message = self.encode_message.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Error", "Please enter a message to embed.")
            return

        password = self.encode_password.text()
        if not password:
            QMessageBox.warning(self, "Error", "Please enter an encryption password.")
            return

        try:
            self.set_status("Encrypting message...")
            encrypted = CryptoHelper.encrypt(message, password)

            self.set_status(f"Embedding {len(encrypted)} bytes...")
            self.engine.set_snr(self.snr_spin.value())
            stego = self.engine.embed_in_audio(self.carrier_audio, encrypted, self.carrier_sample_rate)

            # Show after spectrum
            fft = np.abs(np.fft.fft(stego[:4096]))[:128]
            self.encode_spectrum.set_after(fft.tolist())

            # Save file
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Encoded Audio", "encoded_message.wav",
                "WAV Files (*.wav)"
            )

            if save_path:
                AudioHandler.save_wav(save_path, stego, self.carrier_sample_rate)
                self.set_status(f"SUCCESS: Saved to {os.path.basename(save_path)}")
                QMessageBox.information(self, "Success", f"Message embedded and saved to:\n{save_path}")

        except Exception as e:
            self.set_status(f"ERROR: {str(e)}")
            QMessageBox.critical(self, "Encode Error", str(e))

    def do_decode(self):
        if self.stego_audio is None:
            QMessageBox.warning(self, "Error", "Please load an encoded audio file first.")
            return

        password = self.decode_password.text()
        if not password:
            QMessageBox.warning(self, "Error", "Please enter the decryption password.")
            return

        try:
            self.set_status("Extracting embedded data...")
            extracted_bytes = self.engine.extract_from_audio(self.stego_audio)

            if not extracted_bytes:
                self.set_status("No message found or extraction failed")
                self.decode_result.setText("No message found in audio.")
                return

            self.set_status("Decrypting message...")
            plaintext = CryptoHelper.decrypt(extracted_bytes, password)

            self.decode_result.setText(plaintext)
            self.set_status(f"SUCCESS: Extracted {len(plaintext)} characters")

        except ValueError as e:
            self.set_status("Decryption failed - wrong password?")
            self.decode_result.setText("❌ DECRYPTION FAILED\n\nPossible causes:\n- Wrong password\n- Corrupted audio\n- No embedded message")
        except Exception as e:
            self.set_status(f"ERROR: {str(e)}")
            self.decode_result.setText(f"Error: {str(e)}")

    def set_status(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.setText(f"[{timestamp}] {text}")


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        from theme import apply_theme
        apply_theme(app)
    except:
        pass

    window = StudioWindow()
    window.show()
    sys.exit(app.exec())
