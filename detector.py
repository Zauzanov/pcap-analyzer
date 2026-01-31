import cv2                                                          # pip install opencv-python.
import os  

ROOT = '/home/kali/Desktop/pictures'                                # Source dir containing images to scan.
FACES = '/home/kali/Desktop/faces'                                  # Target output directory where annotated images get saved.
TRAIN = '/usr/share/opencv4/haarcascades'                           # Dir for Haar cascade XML files. On Kali, OpenCV cascades are often pre-installed here.

def detect(srcdir=ROOT, tgtdir=FACES, train_dir=TRAIN):
    if not os.path.exists(tgtdir):                                  # Ensures the output directory exists
        os.makedirs(tgtdir)
        print(f"[*] Created target directory: {tgtdir}")

    cascade_path = os.path.join(train_dir, 
                                'haarcascade_frontalface_alt.xml')  # Builds a path using the OS-specific separator, verifying the Cascade file exists.
    if not os.path.exists(cascade_path):
        print(f"[-] Error: Cannot find {cascade_path}")
        print("    Try: sudo apt install libopencv-dev")
        return

    face_cascade = cv2.CascadeClassifier(cascade_path)              # Initializes the classifier and loads a pre-trained model.
    found_count = 0                                                 # Initializes a counter.

    print(f"[*] Scanning {srcdir} for faces...")

    # Iterates through files in source directory, 
    # one filename per iteration: 
    for fname in os.listdir(srcdir):                                # Extension check, making the filename lowercase.
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue                                                # If it does'nt end with these extenstions, skip the rest of this loop body and move to the next file. 
        
        # Build full input and output paths
        fullname = os.path.join(srcdir, fname)                      # full path to the source image.
        newname = os.path.join(tgtdir, fname)                       # full path where output will be written using the same filename.
        
        img = cv2.imread(fullname)                                  # Reads the image file at fullname.
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                # Converts to Grayscale for the detector.
        
        # Detection rules:
        # scaleFactor=1.3: how much the image size is reduced at each image scale.
        # minNeighbors=5: how many neighbors each candidate rectangle should have to retain it.
        rects = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # If any faces found in this image
        if len(rects) > 0:
            print(f" [+] Found face in {fname}!")
            found_count += 1
            
            # Draws rectangles on the original image
            for (x, y, w, h) in rects:
                cv2.rectangle(img, (x, y), (x + w, y + h), (127, 255, 0), 2)
                # Edit:
                # color = (127, 255, 0) in BGR order: That is: Blue=127, Green=255, Red=0 (a bright green line);
                # thickness = 2 means 2 pixels wide: If thickness were -1, it would fill the rectangle.
            
            # Saves the modified image:
            success = cv2.imwrite(newname, img)
            if not success:
                print(f" [!] Failed to save {newname}")

    print(f"[*] Detection complete. Found {found_count} faces.")

if __name__ == '__main__':
    detect()

