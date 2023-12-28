# File Upload Server

This is a simple file upload server implemented in Python using the Flask framework.

## Features

- Allows users to upload files to the server in other word file sharing app.
- Provides an admin panel with options like QR code generation (QR of upload page URL).

## Getting Started

### Prerequisites

- Python (3.x recommended)
- Flask (install via `pip install Flask`)
- python server.py

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RKDhakad/FileUploadServer.git
   cd FileUploadServer

### Usage
1. Access the admin panel by visiting http://127.0.0.1:5000/admin in your browser.
2. Enter the admin password to log in.
3. On the admin panel, you can find options to generate a QR code for the upload page and view the upload page URL.
4. Users can access the upload page at http://<serverip>:5000/upload to upload files.

### Configuration
Modify the app.config['UPLOAD_FOLDER'] variable in server.py to set the default upload folder.

### Important Note
This application is designed to work within the local area network (LAN).
