import cv2
import numpy as np

class Background:

    def __init__(self):
        self.count = 0

    def set_background(self):
        """
        Generate background video
        """
        cam = cv2.VideoCapture(0)
        if (cam.isOpened() == False): 
            print("Error reading video")
        frame_width = int(cam.get(3))
        frame_height = int(cam.get(4))
        size = (frame_width, frame_height)
        input("Press enter to take background video")
        result = cv2.VideoWriter('./background_video.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
        for i in range(60):
            ret, frame = cam.read()
            if ret == True: 
                result.write(frame)
                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break
            else:
                break
        # for background video, create the background image
        capture = cv2.VideoCapture('./background_video.avi')
        frameIds = capture.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)
        frames = []
        for frame_id in frameIds:
            capture.set(cv2.CAP_PROP_FRAME_COUNT, frame_id)
            ret, frame = capture.read()
            frames.append(frame)
        median_frame = np.median(frames, axis=0).astype(dtype=np.uint8)
        cv2.imwrite('./background_frame.jpg', median_frame)
        cam.release()
        result.release()
        cv2.destroyAllWindows()