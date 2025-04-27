from flask import Flask, render_template, request, send_file, url_for
import qrcode
import os
import io   
from werkzeug.utils import secure_filename
import threading
import time

app = Flask(__name__)

# Create 'uploads' directory if it doesn't exist
uploads_dir = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

def delete_old_file(filename):
    """Delete the file after 5 minutes"""
    filepath = os.path.join(uploads_dir, filename)
    try:
        os.remove(filepath)
        print(f"Deleted {filename}")
    except Exception as e:
        print(f"Error deleting file: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.get('data')

    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    # Save the image temporarily in 'uploads' folder
    filename = secure_filename(f"qr_{data}.png")
    filepath = os.path.join(uploads_dir, filename)
    img.save(filepath)

    # Set a timer to delete the file after 5 minutes (300 seconds)
    threading.Timer(180, delete_old_file, [filename]).start()

    return render_template('index.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(uploads_dir, filename))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(uploads_dir, filename), as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
