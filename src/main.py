# Importing all the needed packages
from tensorflowfunction import *
from bluetoothcommunication import *
from tkinter import *
from tkinter.font import *
from pyttsx3 import *
from threading import * 
import sys
val = ""
# config all the tkinter window 
rootWindow = Tk()
rootWindow.iconphoto(False, PhotoImage(file = "src/pics/eye.png"))
rootWindow.title("Third eye")
rootWindow.geometry("500x500")
rootWindow.resizable(False, False)
rootWindow.config(bg = "#a7c5eb")
# initializing the tts
robotVoice = init()
buttonFont = Font(weight = "bold",size = 38)
def welcome():
    robotVoice.say("Third eye started")
    robotVoice.runAndWait()
welcomeThread = Thread(target=welcome).start()



def detect():
    MODEL_PATH = os.path.join("src/frozen_inference_graph.pb")
    CONFIG_PATH = os.path.join("src/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    LABELS_PATH = os.path.join("src/labels.txt")
    SCORE_THRESHOLD = 0.6
    NETWORK_INPUT_SIZE = (300, 300)
    NETWORK_SCALE_FACTOR = 1

    logger = logging.getLogger('detector')
    logging.basicConfig(level=logging.INFO)

    # Reading coco labels
    with open(LABELS_PATH, 'rt') as f:
        labels = f.read().rstrip('\n').split('\n')
    logger.info(f'Available labels: \n{labels}\n')
    COLORS = np.random.uniform(0, 255, size=(len(labels), 3))

    # Loading model from file
    logger.info('Loading model from tensorflow...')
    ssd_net = cv2.dnn.readNetFromTensorflow(model=MODEL_PATH, config=CONFIG_PATH)
    # Initiating camera
    logger.info('Starting video stream...')
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()

    while True:
        # Reading frames
        frame = vs.read()
        frame = imutils.resize(frame, width=1200)
        height, width, channels = frame.shape

        # Converting frames to blobs using mean standardization
        blob = cv2.dnn.blobFromImage(image=frame,
                                    scalefactor=NETWORK_SCALE_FACTOR,
                                    size=NETWORK_INPUT_SIZE,
                                    mean=(127.5, 127.5, 127.5),
                                    crop=False)

        # Passing blob through neural network
        ssd_net.setInput(blob)
        network_output = ssd_net.forward()

        # Looping over detections
        for detection in network_output[0, 0]:
            score = float(detection[2])
            class_index = np.int(detection[1])
            label = f'{labels[class_index]}: {score:.2%}'

            # Drawing likely detections
            if score > SCORE_THRESHOLD:
                left = np.int(detection[3] * width)
                top = np.int(detection[4] * height)
                right = np.int(detection[5] * width)
                bottom = np.int(detection[6] * height)

                cv2.rectangle(img=frame,
                            rec=(left, top, right, bottom),
                            color=COLORS[class_index],
                            thickness=4,
                            lineType=cv2.LINE_AA)
                
                # robotVoice.say("in front of you there is a "+label)
                
                cv2.putText(img=frame,
                            text=label,
                            org=(left, np.int(top*0.9)),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=2,
                            color=COLORS[class_index],
                            thickness=2,
                            lineType=cv2.LINE_AA)
                print(label)
                robotVoice.say("there is "+label)
                robotVoice.runAndWait()
        cv2.imshow("Detector", frame)
        

        # Exit loop by pressing "q"
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        fps.update()

    fps.stop()
    logger.info(f'\nElapsed time: {fps.elapsed() :.2f}')
    logger.info(f' Approx. FPS: {fps.fps():.2f}')
    cv2.destroyAllWindows()
    vs.stop()

# robotVoiceThread = Thread(target=say, args=mes).start()



startBu = Button(rootWindow, text = "Start using camera", bg = "#709fb0", fg = "white", font = buttonFont, command =detect)
startBu.grid(row = 0, column = 0)
rootWindow.mainloop()
sys.exit()