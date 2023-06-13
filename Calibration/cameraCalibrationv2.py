import numpy as np
import cv2 as cv
import glob

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

chessboardSize = (12, 8)
frameSize = (1280, 720)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

size_of_chessboard_squares_mm = 30
objp *= size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
objpoints = []  # 3D point in real-world space
imgpoints = []  # 2D points in the image plane.

images = glob.glob('calibration_images/*.jpg')

for image in images:
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None, cv.CALIB_CB_FAST_CHECK)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)  # Use refined corners

cv.destroyAllWindows()

############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, frameSize, None, None
)


############## UNDISTORTION #####################################################

def undistort_image(frame):
    h, w = frame.shape[:2]
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, frameSize)

    # Undistort
    dst = cv.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)

    # Crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]

    # Check if the resulting image is valid
    if dst.shape[0] > 0 and dst.shape[1] > 0:
        dst = cv.resize(dst, frameSize)
        return dst
    else:
        return None
################ CONTINUOUS UNDISTORTION ########################################
def continuous_undistortion():
    cap = cv.VideoCapture(1,cv.CAP_DSHOW)  # Use 0 or the appropriate camera index
    while True:
        ret, frame = cap.read()
        if ret:
            undistorted_frame = undistort_image(frame)
            # Check if the undistorted frame is valid
            if undistorted_frame is not None:
                cv.imshow('Undistorted Image', undistorted_frame)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
continuous_undistortion()
