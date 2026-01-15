from fpdf import FPDF
import datetime

class MethodologyPaper(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Milcodec Project: Technical Methodology', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + ' | CONFIDENTIAL - EYES ONLY', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, label, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('Times', '', 12)
        self.multi_cell(0, 10, text)
        self.ln()
        
    def code_block(self, code):
        self.set_font('Courier', '', 10)
        self.set_fill_color(240, 240, 240)
        self.multi_cell(0, 5, code, 1, 'L', True)
        self.ln()

pdf = MethodologyPaper()
pdf.add_page()
pdf.set_title("Milcodec Methodology")
pdf.set_author("Senior Defense Architect")

# ABSTRACT
pdf.set_font('Times', 'B', 14)
pdf.cell(0, 10, 'Abstract', 0, 1, 'C')
pdf.set_font('Times', '', 12)
pdf.multi_cell(0, 10, 'This paper details the architecture and implementation of the Milcodec System, a covert signaling platform designed for field operations. The system utilizes Direct Sequence Spread Spectrum (DSSS) steganography to hide encrypted command data within a -20dB noise floor, effectively bypassing standard intercept methods. The platform consists of a receiver ("Night Watch") and a transmission commander ("Glass Cockpit"), both secured by a simulated Post-Quantum Cryptography (PQC) layer.')
pdf.ln(10)

# 1. INTRODUCTION
pdf.chapter_title('1. Introduction')
pdf.chapter_body('Modern battlefield communications face the constant threat of Electronic Warfare (EW) jamming and interception. Traditional encryption is necessary but insufficient if the transmission itself is detected. The Milcodec project aims to solve this by achieving "Low Probability of Intercept" (LPI) properties via steganography.')
pdf.chapter_body('The system hides low-bandwidth command data (approx. 32 bps) underneath a carrier signal that mimics Gaussian noise, rendering it indistinguishable from background static to casual observers.')

# 2. SIGNAL PROCESSING ARCHITECTURE
pdf.chapter_title('2. Signal Processing Architecture')
pdf.chapter_body('The core of the system is the implementation of DSSS (Direct Sequence Spread Spectrum).')

pdf.set_font('Times', 'B', 12)
pdf.cell(0, 10, '2.1 Spreading Algorithm', 0, 1)
pdf.chapter_body('We utilize a 31-bit pseudo-noise code (PNC), specifically a Barker-like M-sequence, to spread the spectrum of the input data. The spreading factor (SF) is 31.')
pdf.code_block('PNC_KEY = [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, ...]\nInput Bit (0/1) -> Mapped to +/- 1\nSpread Chip Sequence = Input_Scalar * PNC_KEY')

pdf.set_font('Times', 'B', 12)
pdf.cell(0, 10, '2.2 Masking and Modulation', 0, 1)
pdf.chapter_body('The spread chips are modulated onto a 12kHz carrier wave using simple amplitude modulation (Simulated BPSK). To achieve covertness, the signal is mixed with high-amplitude Gaussian noise.')
pdf.chapter_body('The mathematical model for the transmitted signal S(t) is:')
pdf.code_block('S_tx(t) = 0.1 * S_mod(t) + 0.9 * N(t)\n\nWhere:\n- S_mod(t) is the modulated data signal\n- N(t) is Gaussian White Noise')
pdf.chapter_body('This results in an effective Signal-to-Noise Ratio (SNR) of approximately -20dB, burying the data below the noise floor.')

# 3. CRYPTOGRAPHIC LAYER
pdf.chapter_title('3. Cryptographic Layer')
pdf.chapter_body('Security is handled by a hybrid "Store-and-Burn" architecture.')
pdf.chapter_body('- **Key Exchange**: Simulated CRYSTALS-Kyber KEM is used for ephemeral session key establishment.\n- **Payload Encryption**: ChaCha20-Poly1305 provides high-speed, authenticated symmetric encryption.\n- **Burn Protocol**: A dedicated "Panic" subroutine (Protocol Zero) allows immediate wiping of private keys from RAM.')

# 4. IMPLEMENTATION DETAILS
pdf.chapter_title('4. Implementation Details')
pdf.chapter_body('The system is implemented in Python, leveraging `numpy` for vector math and `PyQt6` for the tactical interface. The architecture is split into three standalone modules:')
pdf.chapter_body('1. **milcodec_receiver.py**: The "Night Watch" field unit.\n2. **milcodec_commander.py**: The C2 uplink terminal.\n3. **milcodec_masker.py**: The standalone signal masking engine.')

# 5. CONCLUSION
pdf.chapter_title('5. Conclusion')
pdf.chapter_body('The Milcodec system successfully demonstrates that high-security, low-probability-of-intercept communications can be achieved using standard consumer hardware. The -20dB noise floor masking provides a robust layer of obfuscation, ensuring that field commands can be received securely even in contested electromagnetic environments.')

# Output
pdf.output("Milcodec_Methodology_Paper.pdf")
print("PDF Generated Successfully.")
