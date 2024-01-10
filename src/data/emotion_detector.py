from deepface import DeepFace
import cv2
import time
from src.data.models.emotion import EmotionStats


class EmotionDetector:

    def __init__(self):
        self.continue_detection = False

    def stop_detection(self):
        self.continue_detection = True

    def start_detection(self, interval_secs, callback):
        self.continue_detection = False

        # Open the webcam
        cap = cv2.VideoCapture(0)

        while True:
            if self.continue_detection:
                break

            # Capture frame-by-frame
            _, frame = cap.read()

            try:
                # Perform emotion detection using DeepFace
                result = DeepFace.analyze(frame, actions=['emotion'], silent=True)

                # Extract the emotion
                emotion = result[0]

                #print(emotion)
                callback(EmotionStats(emotion))
                #print('callback called')

                # Display the emotion
                #cv2.putText(frame, f'Emotion: {emotion}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # Display the resulting frame
                #cv2.imshow('Emotion Detection', frame)

                # Break the loop when 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as e:
                print(e)
                print("No face detected")

            # Break the loop when stop_detection is True
            time.sleep(interval_secs)

        # Release the webcam and close all windows
        cap.release()
        cv2.destroyAllWindows()
