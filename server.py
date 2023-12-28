from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
from io import BytesIO
import socket
import qrcode
import platform
import os

app = Flask(__name__)

# Configuration
def get_os():
    system = platform.system()
    
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        # Check for specific Linux distributions
        try:
            with open("/etc/os-release", "r") as os_release_file:
                lines = os_release_file.readlines()
                for line in lines:
                    if line.startswith("ID="):
                        distro_id = line.split("=")[1].strip().lower()
                        if distro_id == "kali":
                            return "Kali Linux"
                        elif distro_id == "ubuntu":
                            return "Ubuntu"
        except FileNotFoundError:
            pass  # /etc/os-release file not found, treat it as generic Linux
        
        # Check for Termux
        if "termux" in os.environ.get("SHELL", "").lower():
            return "Termux"

    elif system == "Darwin":
        return "macOS"
    else:
        return "Unknown"
    
if get_os()=="Windows":
    UPLOAD_FOLDER = 'uploads'
elif get_os()=="Termux":
    UPLOAD_FOLDER = '/sdcard/DCIM/Termux Server'

if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'rar', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key

# Password for admin panel (change this to a secure password)
ADMIN_PASSWORD = 'admin'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload_page.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return render_template('admin_panel.html')
        else:
            return "Invalid password"
    return render_template('admin_login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        files = request.files.getlist('file')
        
        for file in files:
            if file.filename == '':
                return jsonify({'error': 'No selected file'})
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return jsonify({'message': 'Files uploaded successfully'})

    # If it's a GET request, return the upload page
    return render_template('upload_page.html')

@app.route('/generate_qr_code')
def generate_qr_code():
    if 'logged_in' not in session or not session['logged_in']:
        return "Unauthorized", 403

    ip_address = get_local_ip()
    port = 5000
    upload_page_url = f"http://{ip_address}:{port}/upload"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upload_page_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

def get_local_ip():
    try:
        # Create a socket connection to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Connect to Google's public DNS server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return '127.0.0.1' 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
