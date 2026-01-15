# MILCODEC SYSTEM v2.0

<div align="center">
  
**COVERT SIGNALING PLATFORM FOR FIELD OPERATIONS**

*Direct Sequence Spread Spectrum Steganography • Post-Quantum Cryptography • Low Probability of Intercept*

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/UI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![ChaCha20](https://img.shields.io/badge/Crypto-ChaCha20--Poly1305-red.svg)](https://en.wikipedia.org/wiki/ChaCha20-Poly1305)

</div>

---

## 🎯 Overview

Milcodec is a **military-grade covert communication system** that hides encrypted command data within audio signals, achieving a **-20dB noise floor masking** that renders transmissions indistinguishable from background static.

### Key Features

| Feature | Description |
|---------|-------------|
| **DSSS Steganography** | 31-bit PN code spreading for robust signal hiding |
| **-20dB Masking** | Signal buried 100x below noise floor |
| **Post-Quantum Ready** | Simulated CRYSTALS-Kyber KEM + ChaCha20-Poly1305 |
| **Audio Steganography** | Embed messages in music/audio files |
| **Multi-Channel TX** | TCP, Radio (WAV), FM, Internet Radio |
| **Protocol Zero** | Emergency key wipe with confirmation |

---

## 📦 Components

### 1. Night Watch Receiver (`milcodec_receiver.py`)
Field unit terminal for signal reception and decryption.

- Real-time SNR visualization with gradient graph
- Priority-colored message feed (FLASH/IMMEDIATE/PRIORITY/ROUTINE)
- Multi-source input (Microphone, Network, File, Simulation)
- Protocol Zero panic wipe capability

### 2. Glass Cockpit Commander (`milcodec_commander.py`)
C2 command center for secure transmission.

- Tactical battlespace map with unit tracking
- FFT spectrum analyzer visualization
- Multi-mode transmission (TCP/Radio/FM/Internet)
- Command priority selection
- Unit roster management

### 3. Studio (`milcodec_studio.py`)
Audio steganography suite for covert messaging.

- Drag-and-drop audio file loading
- Encrypt messages into songs/audio files
- Extract and decrypt hidden messages
- Spectrum before/after comparison
- Configurable SNR (-10dB to -30dB)

### 4. Masker Engine (`milcodec_masker.py`)
Core DSSS signal processing library.

- CLI interface for batch processing
- Carrier embedding for steganography
- Signal analysis utilities

---

## 🚀 Quick Start

### Installation

```powershell
# Clone or download the project
cd Milcodec

# Install dependencies
pip install -r requirements.txt

# Optional: Install PyAudio for live microphone input (Windows)
pip install pyaudio
```

### Run Applications

```powershell
# Start the Receiver (Field Unit)
python milcodec_receiver.py

# Start the Commander (C2 Terminal)
python milcodec_commander.py

# Start the Studio (Audio Steganography)
python milcodec_studio.py

# Or use the launcher script
start_mission.bat
```

---

## 🔐 Security Architecture

### Encryption Layer

```
┌─────────────────────────────────────────────────────────┐
│                    CRYPTO ENGINE                        │
├─────────────────────────────────────────────────────────┤
│  1. CRYSTALS-Kyber KEM (Simulated)                     │
│     └─ Post-quantum secure key encapsulation           │
│                                                         │
│  2. ChaCha20-Poly1305                                  │
│     └─ High-speed authenticated encryption             │
│                                                         │
│  3. PBKDF2-SHA256                                      │
│     └─ 100,000 iterations key derivation               │
└─────────────────────────────────────────────────────────┘
```

### Signal Processing

```
┌─────────────────────────────────────────────────────────┐
│                  DSSS PIPELINE                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Plaintext ──► Encrypt ──► Bytes ──► Bits              │
│                                        │                │
│                              ┌─────────▼─────────┐      │
│                              │   PN Spreading    │      │
│                              │   (31-chip code)  │      │
│                              └─────────┬─────────┘      │
│                                        │                │
│                              ┌─────────▼─────────┐      │
│                              │  BPSK Modulation  │      │
│                              │   (12kHz carrier) │      │
│                              └─────────┬─────────┘      │
│                                        │                │
│                              ┌─────────▼─────────┐      │
│                              │  Noise Masking    │      │
│                              │    (-20dB SNR)    │      │
│                              └─────────┬─────────┘      │
│                                        │                │
│                                        ▼                │
│                               Audio Output              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📡 Transmission Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **TCP** | Direct network transmission | LAN/VPN operations |
| **RADIO** | Save as WAV for radio broadcast | HF/VHF transmission |
| **FM** | FM-optimized audio output | Commercial FM embedding |
| **INTERNET** | Stream to Icecast/Shoutcast | Internet radio cover |

---

## 🎨 UI Design

The interface follows **Palantir Gotham** design principles:

- **Dark Theme**: Deep backgrounds (#0d0d14, #14141f)
- **Accent Colors**: Cyan (#00d4ff), Amber (#ffb000), Green (#00ff88)
- **Typography**: Inter (UI), JetBrains Mono (code/data)
- **Effects**: Gradient fills, subtle glow, animated indicators

---

## 📁 File Structure

```
Milcodec/
├── milcodec_receiver.py    # Night Watch - Field Receiver
├── milcodec_commander.py   # Glass Cockpit - C2 Commander
├── milcodec_studio.py      # Audio Steganography Suite
├── milcodec_masker.py      # DSSS Signal Engine
├── theme.py                # UI Design System
├── requirements.txt        # Python Dependencies
├── start_mission.bat       # Windows Launcher
└── README.md              # This Document
```

---

## ⚠️ Classification Notice

```
┌────────────────────────────────────────────────────────┐
│                    UNCLASSIFIED                        │
│         FOR DEMONSTRATION PURPOSES ONLY                │
│                                                        │
│  This software is a proof-of-concept implementation.   │
│  Real military applications require additional:        │
│  - Hardware security modules (HSM)                     │
│  - FIPS 140-3 validated cryptography                   │
│  - Proper key management infrastructure                │
│  - Security certification & accreditation              │
└────────────────────────────────────────────────────────┘
```

---

## 📋 Requirements

- Python 3.9+
- PyQt6 6.4+
- NumPy
- Cryptography library
- PyAudio (optional, for live microphone)
- SciPy (for advanced signal processing)

---

## 📜 License

Proprietary - All Rights Reserved

---

<div align="center">
  
**MILCODEC v2.0** • *Secure Communications for Contested Environments*

</div>
