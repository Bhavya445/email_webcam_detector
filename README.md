# Email Webcam Motion Detector

A simple Python project that uses OpenCV to detect motion via webcam and emails an image of the detected motion.

## Features
- Motion detection using OpenCV
- Sends email with captured frame when motion is detected
- Threaded execution to avoid UI freeze
- Automatic cleanup of images folder

## Setup

### 1. Clone and Install

```bash



git clone https://github.com/Bhavya445/email-webcam-detector.git
cd email-webcam-detector
pip install -r requirements.txt
2. Configure .env
Create a .env file in the root directory:

ini
Copy
Edit
EMAIL_SENDER=your_email@gmail.com
EMAIL_RECEIVER=receiver_email@gmail.com
EMAIL_PASSWORD=your_generated_app_password
💡 Use a Gmail App Password, not your real password.

3. Run the App
bash
Copy
Edit
python main.py
Press q to quit the video window.