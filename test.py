import cv2
from picamera2 import Picamera2
import time

def capture_photo():
    # Initialize Picamera2
    picam2 = Picamera2()
    
    # Configure the camera
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
    picam2.start()
    
    # Allow the camera to warm up
    time.sleep(2)
    
    # Capture the image using OpenCV
    frame = picam2.capture_array()
    
    # Show the image using OpenCV
    cv2.imshow('Captured Image', frame)
    
    # Save the image
    cv2.imwrite('captured_image.jpg', frame)
    print("Image saved as captured_image.jpg")
    
    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Stop the camera
    picam2.stop()

if __name__ == "__main__":
    capture_photo()
