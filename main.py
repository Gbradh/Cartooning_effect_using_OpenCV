import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw
import matplotlib.pyplot as plt
import os

baseDirectory = os.getcwd()

cap = cv2.VideoCapture(0)


def Proj_ect():
    print("BROWSING PRESS B")
    print("OPEN-WEBCAM PRESS C")
    print("APPLY FILTER PRESS A")
    print("TO SEE FILTERS AVAILABLE BUT NOT IN USE PRESS I")
    print("Quite PRESS Q")


def select_image():
    global panelA, panelB
    # image
    path = filedialog.askopenfilename()

    # ensure a file path was selected
    if len(path) > 0:
        # load the image from disk, convert it to grayscale, and detect
        # edges in it
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        color = cv2.bilateralFilter(image, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        cv2.imwrite(os.path.join(baseDirectory, 'cache\img.JPG'), cartoon)

    # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        edged = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)

        # convert the images to PIL format...
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        # ...and then to ImageTk format
        resize_image = image.resize((450, 350))
        resize_edged = edged.resize((450, 350))

        image = ImageTk.PhotoImage(resize_image)
        edged = ImageTk.PhotoImage(resize_edged)

    # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = tk.Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
            # while the second panel will store the edge map
            panelB = tk.Label(image=edged)
            panelB.image = edged
            panelB.pack(side="right", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image = image
            panelB.image = edged


def sample_Code():

    ddepth = cv2.CV_8U
    kernel_size = 300
    img = cv2.imread(os.path.join(baseDirectory, 'cache\Sample.JPG'))

    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # MedianFilter to Reduce Noise DIDN"T FIND SMOOTH()
    median = cv2.medianBlur(grayImage, 7)
    # Kernel Size is not doing any difference
    Laplaced = cv2.Laplacian(median, ddepth, kernel_size)
    ret, thresh = cv2.threshold(Laplaced, 5, 125, cv2.THRESH_BINARY)

    thresh = 255-thresh
    thresh2 = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    small = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

    painting = cv2.bilateralFilter(small, 9, 75, 75)

    painting_resized = cv2.resize(
        painting, (thresh2.shape[1], thresh2.shape[0]))

    print("My thresh2 is ", thresh2.shape)
    print("My painting_resized is ", painting_resized.shape)
    print("My painting is ", painting.shape)

    dst = cv2.bitwise_and(painting_resized, thresh2)
    # cv2.imshow('dst',dst)
    # cv2.imshow('image',img)

    # same window showing

    titles = ['Original Image', 'Gray', 'Medained', 'thresh',
              'Laplaced', 'small', 'painting', 'dst', 'Cartoon']
    images = [img, grayImage, median, thresh2,
              Laplaced, small, painting, dst, cartoon]

    for i in range(9):
        plt.subplot(3, 3, i+1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    mng = plt.get_current_fig_manager()  # maximizing window size
    mng.resize(*mng.window.maxsize())  # maximizing window size
    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def OpenFile():
    name = askopenfilename(initialdir="C:\\Users\\gurba",
                           filetypes=(("jpg File", "*.jpg"), ("png File", "*.png"),
                                      ("JPG File", "*.JPG"), ("PNG File", "*.PNG"), ("All Files", "*.*")),
                           title="Choose a file.")
    print(name)

    # Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name, 'r'):
            img = cv2.imread(name, 1)
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.imshow('image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    except:
        print("***************NONE****************")


def savefile():
    file1 = [("jpg File", "*.jpg"), ("png File", "*.png"),
             ("JPG File", "*.JPG"), ("PNG File", "*.PNG"), ("All Files", "*.*")]
    filename = filedialog.asksaveasfile(
        filetypes=file1, mode='w', defaultextension=file1)
    if not filename:
        return
    edge.save(filename)


if __name__ == "__main__":

    Proj_ect()

    while True:

        ans = input("Answer: ")

        if ans == 'q' or ans == 'Q':
            break

        elif ans == 'b' or ans == 'B':
            root = tk.Tk()
            Title = root.title("File Opener")

            # Menu Bar
            menu = tk.Menu(root)
            root.config(menu=menu)
            file = tk.Menu(menu)
            file.add_command(label='Open', command=OpenFile)
            menu.add_cascade(label='File', menu=file)
            btn = tk.Button(root, text="BROWSE IMAGE", command=OpenFile)
            btn.pack(side="bottom", fill="both",
                     expand="yes", padx="10", pady="10")
            root.mainloop()

        elif ans == 'c' or ans == 'C':
            if not cap.isOpened():
                print("Cannot open camera")
                break

            print("CAPTURE PRESS F")
            print("Exit PRESS E")

            while True:

                # Capture frame-by-frame
                ret, frame = cap.read()

                # if frame is read correctly ret is True
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break

                # Our operations on the frame come here
                color = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                cv2.imshow('CAMERA', color)

                if cv2.waitKey(1) == ord('e') or cv2.waitKey(1) == ord('E'):
                    break

                elif cv2.waitKey(1) == ord('f') or cv2.waitKey(1) == ord('F'):
                    root = tk.Tk()
                    img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    edge = Image.fromarray(img)
                    tk_edge = ImageTk.PhotoImage(edge)
                    label = tk.Label(root, image=tk_edge)
                    label.pack()
                    button = tk.Button(
                        root, text="SAVE IMAGE", command=savefile)
                    button.pack(side="bottom", fill="both",
                                expand="yes", padx="10", pady="10")
                    root.mainloop()

                else:
                    continue

            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()

        elif ans == 'a' or ans == 'A':
            # initialize the window toolkit along with the two image panels
            root = tk.Tk()
            panelA = None
            panelB = None
            # create a button, then when pressed, will trigger a file chooser
            # dialog and allow the user to select an input image; then add the
            # button the GUI
            image = cv2.imread(os.path.join(baseDirectory, "cache\img.JPG"))
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            edge = Image.fromarray(img)
            btn = tk.Button(root, text="SELECT IMAGE", command=select_image)
            button = tk.Button(root, text="SAVE IMAGE", command=savefile)
            btn.pack(side="bottom", fill="both",
                     expand="yes", padx="10", pady="10")
            button.pack(side="bottom", fill="both",
                        expand="yes", padx="10", pady="10")
            # kick off the GUI
            root.mainloop()

        elif ans == 'i' or ans == 'I':
            # speak("There is our filters, which is not using now!")
            sample_Code()

        else:
            print("THERE IS A KEY PRESSING MISTAKE KEEP READ AGAIN!")
            print("BROWSING PRESS B")
            print("OPEN-CAMERA PRESS C")
            print("APPLY FILTER PRESS A")
            print("TO SEE FILTERS AVAILABLE BUT NOT IN USE PRESS I")
            print("Quite PRESS Q")
            print("PLEASE TRY AGAIN!")
