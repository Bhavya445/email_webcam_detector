# Updated main.py
import cv2
import time
from emailing import send_email
import glob
import os
from threading import Thread

# Auto-create the images directory
if not os.path.exists("images"):
    os.makedirs("images")
    print("[INFO] Created 'images/' directory")

video = cv2.VideoCapture(0)
first_frame = None
status_list = []
count = 1

def clean_folder():
    print("cf start")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("cf ended")

while True:
    status = 0
    time.sleep(1)
    check, frame = video.read()

    if not check:
        print("Failed to read from webcam.")
        continue

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cv2.imshow("My video", dil_frame)

    contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_with_object = None

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            if all_images:
                index = int(len(all_images) / 2)
                image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0 and image_with_object:
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        email_thread.start()

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()

clean_thread = Thread(target=clean_folder)
clean_thread.daemon = True
clean_thread.start()
