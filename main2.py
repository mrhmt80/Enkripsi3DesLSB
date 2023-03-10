#Enkripsi File PDF Menggunakan Algoritma 3Des
from Crypto.Cipher import DES3
import os

# Set the key and initialization vector for 3DES encryption
key = b'0123456789abcdef01234567'
iv = b'abcdefgh'

# Load the PDF file to be encrypted
filename = 'p.pdf'
with open(filename, 'rb') as f:
    pdf_data = f.read()

# Pad the PDF data to be a multiple of 8 bytes (required for 3DES encryption)
pad_length = 8 - (len(pdf_data) % 8)
pdf_data += bytes([pad_length] * pad_length)

# Create the 3DES cipher object
cipher = DES3.new(key, DES3.MODE_CBC, iv)

# Encrypt the PDF data
encrypted_data = cipher.encrypt(pdf_data)

# Save the encrypted data to a new file
encrypted_filename = os.path.splitext(filename)[0] + '_encrypted.pdf'
with open(encrypted_filename, 'wb') as f:
    f.write(encrypted_data)