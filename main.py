import os
from Crypto.Cipher import DES3
import stegano
from stegano import lsb
from io import BytesIO
from PyPDF4 import PdfFileReader, PdfFileWriter
import zlib

# Generate a 3DES key
key = os.urandom(24)  # generate a 24-byte key

# Read the PDF file and extract the first page
with open('p.pdf', 'rb') as f:
    pdf_reader = PdfFileReader(f)
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pdf_reader.getPage(0))

    # write the output to a BytesIO buffer
    output_buffer = BytesIO()
    pdf_writer.write(output_buffer)

    # get the binary content of the output buffer
    pdf_bytes = output_buffer.getvalue()

# Pad the PDF bytes to a multiple of 8 bytes
padding = b"\0" * (8 - len(pdf_bytes) % 8)
padded_pdf_bytes = pdf_bytes + padding

# Encrypt the PDF bytes using 3DES
cipher = DES3.new(key, DES3.MODE_ECB)
encrypted_pdf_bytes = cipher.encrypt(padded_pdf_bytes)

# Compress the encrypted PDF bytes using zlib
compressed_pdf_bytes = zlib.compress(encrypted_pdf_bytes)

# Embed the compressed and encrypted PDF bytes into the image
cover_image = "coba.png"
output_image = "output.png"
encrypted_image = lsb.hide(cover_image, compressed_pdf_bytes)
encrypted_image.save(output_image)

# To extract the PDF from the image:

# Get the compressed and encrypted PDF bytes from the image
encrypted_image = lsb.reveal(output_image)
compressed_pdf_bytes = zlib.decompress(encrypted_image)

# Decrypt the compressed and encrypted PDF bytes using 3DES
decipher = DES3.new(key, DES3.MODE_ECB)
padded_decrypted_pdf_bytes = decipher.decrypt(compressed_pdf_bytes)

# Remove the padding
decrypted_pdf_bytes = padded_decrypted_pdf_bytes.rstrip(b"\0")

# Write the decrypted PDF bytes to a file
with open('output.pdf', 'wb') as f:
    f.write(decrypted_pdf_bytes)