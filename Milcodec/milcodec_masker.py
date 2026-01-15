"""
MILCODEC DSSS MASKER v2.0 - SIGNAL MASKING ENGINE
===================================================
Professional Direct Sequence Spread Spectrum signal generator.
Supports -10dB to -30dB noise floor masking for covert transmission.
"""

import numpy as np
import wave
import time
import argparse
import sys
import os

# =============================================================================
# CONSTANTS
# =============================================================================
VERSION = "2.0.0"
SAMPLE_RATE = 44100
CARRIER_FREQ = 12000  # 12kHz carrier

# 31-bit Barker-like M-sequence for maximum autocorrelation properties
PNC_KEY = np.array([
    1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,
    0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0
], dtype=np.float32) * 2 - 1

SPREADING_FACTOR = len(PNC_KEY)  # 31
CHIP_DURATION = 0.001  # 1ms per chip
DATA_RATE = 1000 / SPREADING_FACTOR  # ~32 bps

# =============================================================================
# DSSS MASKER CLASS
# =============================================================================
class DSSSMasker:
    """
    Direct Sequence Spread Spectrum signal generator with configurable masking.
    
    Features:
    - Variable SNR from -10dB to -30dB
    - BPSK modulation on 12kHz carrier
    - 31-chip spreading for robustness
    - Audio file embedding support
    """
    
    def __init__(self, snr_db: float = -20, carrier_freq: float = CARRIER_FREQ):
        """
        Initialize DSSS Masker.
        
        Args:
            snr_db: Target signal-to-noise ratio in dB (default -20dB)
            carrier_freq: Carrier frequency in Hz (default 12kHz)
        """
        self.snr_db = max(-30, min(-10, snr_db))
        self.carrier_freq = carrier_freq
        self.sample_rate = SAMPLE_RATE
        
    def set_snr(self, snr_db: float):
        """Set the target SNR for masking."""
        self.snr_db = max(-30, min(-10, snr_db))

    def generate_masked_audio(self, payload_bytes: bytes) -> np.ndarray:
        """
        Generate DSSS-masked audio signal from payload bytes.
        
        Pipeline:
        1. Bytes → Bits
        2. Spreading (Barker Code)
        3. Modulation (BPSK on carrier)
        4. Noise Masking (configurable SNR)
        
        Args:
            payload_bytes: Raw bytes to encode
            
        Returns:
            Masked audio signal as float32 numpy array
        """
        print(f"[MASKER] Processing {len(payload_bytes)} bytes payload (SNR: {self.snr_db}dB)")
        
        # 1. Convert bytes to bits
        bits = self._bytes_to_bits(payload_bytes)
        
        # 2. Apply spreading with PN code
        spread_signal = self._spread_bits(bits)
        
        # 3. Upsample and modulate onto carrier
        modulated = self._modulate_signal(spread_signal)
        
        # 4. Add noise masking at target SNR
        masked = self._apply_noise_masking(modulated)
        
        print(f"[MASKER] Generated {len(masked)} samples ({len(masked)/self.sample_rate:.2f}s)")
        return masked.astype(np.float32)

    def generate_with_carrier(self, payload_bytes: bytes, 
                               carrier_audio: np.ndarray) -> np.ndarray:
        """
        Embed DSSS signal into existing carrier audio (for audio steganography).
        
        Args:
            payload_bytes: Message to embed
            carrier_audio: Existing audio to use as cover
            
        Returns:
            Modified audio with embedded message
        """
        # Generate the modulated signal
        bits = self._bytes_to_bits(payload_bytes)
        spread_signal = self._spread_bits(bits)
        modulated = self._modulate_signal(spread_signal)
        
        # Calculate signal amplitude based on SNR
        carrier_power = np.mean(carrier_audio ** 2)
        snr_linear = 10 ** (self.snr_db / 10)
        signal_amplitude = np.sqrt(carrier_power * snr_linear)
        
        # Ensure modulated signal fits in carrier
        if len(modulated) > len(carrier_audio):
            modulated = modulated[:len(carrier_audio)]
        
        # Add signal to carrier
        output = carrier_audio.copy()
        output[:len(modulated)] += modulated * signal_amplitude
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(output))
        if max_val > 1.0:
            output = output / max_val * 0.99
        
        return output.astype(np.float32)

    def extract_from_audio(self, audio: np.ndarray) -> bytes:
        """
        Extract embedded message from DSSS audio signal.
        
        Args:
            audio: Audio signal with embedded message
            
        Returns:
            Extracted payload bytes
        """
        samples_per_chip = int(self.sample_rate * CHIP_DURATION)
        
        # Demodulate: multiply by carrier
        t = np.linspace(0, len(audio) / self.sample_rate, len(audio))
        carrier = np.sin(2 * np.pi * self.carrier_freq * t)
        demodulated = audio * carrier
        
        # Low-pass filter (simple averaging)
        # TODO: Implement proper matched filter for better performance
        
        # Correlation-based bit detection
        pn_samples = SPREADING_FACTOR * samples_per_chip
        extracted_bits = []
        position = 0
        
        # Extract up to 4096 bits (512 bytes max message)
        max_bits = 4096
        
        while position + pn_samples <= len(demodulated) and len(extracted_bits) < max_bits:
            chunk = demodulated[position:position + pn_samples]
            
            # Downsample to chip rate
            chips = np.array([
                np.mean(chunk[i * samples_per_chip:(i + 1) * samples_per_chip])
                for i in range(SPREADING_FACTOR)
            ])
            
            # Correlate with PN code
            correlation = np.sum(chips * PNC_KEY)
            bit = 1 if correlation > 0 else 0
            extracted_bits.append(bit)
            
            position += pn_samples
        
        # Convert bits to bytes
        return self._bits_to_bytes(extracted_bits)

    def _bytes_to_bits(self, data: bytes) -> list:
        """Convert bytes to list of bits."""
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        return bits

    def _bits_to_bytes(self, bits: list) -> bytes:
        """Convert list of bits back to bytes."""
        byte_list = []
        for i in range(0, len(bits), 8):
            if i + 8 > len(bits):
                break
            byte_bits = bits[i:i + 8]
            byte_val = sum(b << (7 - j) for j, b in enumerate(byte_bits))
            byte_list.append(byte_val)
        return bytes(byte_list)

    def _spread_bits(self, bits: list) -> np.ndarray:
        """Apply PN code spreading to bits."""
        spread_seq = []
        for bit in bits:
            scalar = 1 if bit == 1 else -1
            spread_seq.extend(PNC_KEY * scalar)
        return np.array(spread_seq, dtype=np.float32)

    def _modulate_signal(self, spread_signal: np.ndarray) -> np.ndarray:
        """Upsample and modulate onto carrier frequency (BPSK)."""
        samples_per_chip = int(self.sample_rate * CHIP_DURATION)
        baseband = np.repeat(spread_signal, samples_per_chip)
        
        # Generate carrier wave
        t = np.linspace(0, len(baseband) / self.sample_rate, len(baseband))
        carrier = np.sin(2 * np.pi * self.carrier_freq * t)
        
        # BPSK modulation
        return baseband * carrier

    def _apply_noise_masking(self, modulated: np.ndarray) -> np.ndarray:
        """Add Gaussian noise at target SNR."""
        sig_power = np.mean(modulated ** 2)
        if sig_power == 0:
            sig_power = 1e-9
        
        # Calculate noise power for target SNR
        # SNR_db = 10 * log10(sig_power / noise_power)
        # noise_power = sig_power / 10^(SNR_db/10)
        snr_linear = 10 ** (self.snr_db / 10)
        noise_power = sig_power / snr_linear
        noise_std = np.sqrt(noise_power)
        
        # Generate noise
        noise = np.random.normal(0, noise_std, len(modulated))
        
        # For very low SNR, we want signal buried under noise
        # Mix signal and noise
        masked = modulated + noise
        
        # Normalize
        max_val = np.max(np.abs(masked))
        if max_val > 0:
            masked = masked / max_val * 0.95
        
        return masked

    def save_wav(self, audio_data: np.ndarray, filename: str = "output_masked.wav"):
        """Save audio data to WAV file."""
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            scaled = audio_data / max_val * 32767
        else:
            scaled = audio_data * 32767
        
        scaled = np.int16(scaled)
        
        with wave.open(filename, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(scaled.tobytes())
        
        print(f"[MASKER] Saved to: {filename}")
        return filename


# =============================================================================
# SIGNAL ANALYZER (for debugging/verification)
# =============================================================================
class SignalAnalyzer:
    """Tools for analyzing DSSS signals."""
    
    @staticmethod
    def calculate_snr(original: np.ndarray, noisy: np.ndarray) -> float:
        """Calculate actual SNR between original and noisy signal."""
        if len(original) != len(noisy):
            min_len = min(len(original), len(noisy))
            original = original[:min_len]
            noisy = noisy[:min_len]
        
        noise = noisy - original
        sig_power = np.mean(original ** 2)
        noise_power = np.mean(noise ** 2)
        
        if noise_power == 0:
            return float('inf')
        
        snr_db = 10 * np.log10(sig_power / noise_power)
        return snr_db

    @staticmethod
    def compute_fft(audio: np.ndarray, n_bins: int = 256) -> np.ndarray:
        """Compute FFT magnitude spectrum."""
        fft = np.fft.fft(audio[:4096])
        magnitude = np.abs(fft)[:n_bins]
        return magnitude

    @staticmethod
    def detect_carrier(audio: np.ndarray, sample_rate: int = SAMPLE_RATE) -> float:
        """Detect the carrier frequency in the signal."""
        fft = np.fft.fft(audio)
        freqs = np.fft.fftfreq(len(audio), 1/sample_rate)
        
        # Find peak in positive frequencies
        positive_mask = freqs > 0
        positive_freqs = freqs[positive_mask]
        positive_mags = np.abs(fft)[positive_mask]
        
        peak_idx = np.argmax(positive_mags)
        return positive_freqs[peak_idx]


# =============================================================================
# CLI INTERFACE
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description=f"Milcodec DSSS Masking Tool v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python milcodec_masker.py -t "SECRET MESSAGE" -o broadcast.wav
  python milcodec_masker.py -t "ORDERS" -s -25 -o covert.wav
  python milcodec_masker.py -c carrier.wav -t "HIDDEN" -o stego.wav
        """
    )
    
    parser.add_argument("-t", "--text", type=str, required=True,
                        help="Text message to encode and mask")
    parser.add_argument("-o", "--output", type=str, default="masked_signal.wav",
                        help="Output WAV filename (default: masked_signal.wav)")
    parser.add_argument("-s", "--snr", type=float, default=-20,
                        help="Target SNR in dB (default: -20, range: -30 to -10)")
    parser.add_argument("-c", "--carrier", type=str, default=None,
                        help="Optional carrier audio file for steganography")
    parser.add_argument("-f", "--freq", type=float, default=12000,
                        help="Carrier frequency in Hz (default: 12000)")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {VERSION}")

    args = parser.parse_args()

    # Initialize masker
    masker = DSSSMasker(snr_db=args.snr, carrier_freq=args.freq)

    # Encode the message
    payload = args.text.encode('utf-8')
    print(f"[MASKER] Message: '{args.text}' ({len(payload)} bytes)")
    print(f"[MASKER] Target SNR: {args.snr} dB")
    print(f"[MASKER] Carrier Freq: {args.freq} Hz")

    if args.carrier:
        # Steganography mode
        print(f"[MASKER] Loading carrier: {args.carrier}")
        try:
            with wave.open(args.carrier, 'r') as wf:
                raw_data = wf.readframes(wf.getnframes())
                carrier_audio = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32767
            
            audio = masker.generate_with_carrier(payload, carrier_audio)
        except Exception as e:
            print(f"[ERROR] Failed to load carrier: {e}")
            sys.exit(1)
    else:
        # Pure noise masking mode
        audio = masker.generate_masked_audio(payload)

    # Save output
    masker.save_wav(audio, args.output)
    print(f"[MASKER] Complete!")


if __name__ == "__main__":
    main()
