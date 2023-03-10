#Enkripsi PDF Menggunakan Algoritma 3Des Dan LSB (Steganografi)

from Crypto.Cipher import DES3
from stegano import lsb
import os

# Set the key and initialization vector for 3DES encryption
key = b'0123456789abcdef01234567'
iv = b'abcdefgh'

# Load the PDF file to be encrypted
pdf_filename = 'undangan.pdf'
with open(pdf_filename, 'rb') as f:
    pdf_data = f.read()

# Pad the PDF data to be a multiple of 8 bytes (required for 3DES encryption)
pad_length = 8 - (len(pdf_data) % 8)
pdf_data += bytes([pad_length] * pad_length)

# Create the 3DES cipher object and encrypt the PDF data
cipher = DES3.new(key, DES3.MODE_CBC, iv)
encrypted_data = cipher.encrypt(pdf_data)

# Load the carrier image to hide the encrypted PDF within it
carrier_filename = 'coba.png'

# Embed the encrypted PDF data within the carrier image using LSB steganography
secret = lsb.hide(carrier_filename, encrypted_data)

# Save the steganographed image with the encrypted PDF within it
stego_filename = os.path.splitext(carrier_filename)[0] + '_stego.png'
secret.save(stego_filename)