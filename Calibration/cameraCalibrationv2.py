
import numpy as np
import cv2 as cv
import glob

# Chessboard calibration, from size and number of squares
chessboardSize = (12, 8)
frameSize = (1280, 720)

# Termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

size_of_chessboard_squares_mm = 30
objp *= size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
objpoints = []  # 3D point in real-world space
imgpoints = []  # 2D points in the image plane.

images = glob.glob('Calibration/calibration_images/*.jpg')
print(images)  # Print the list of image filenames for verification
print("Amount of images: ", len(images))

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

if len(objpoints) > 0 and len(imgpoints) > 0:
    ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv.calibrateCamera(
        objpoints, imgpoints, frameSize, None, None
    )
    print("Camera calibration successful!")
else:
    print("Camera calibration failed. Insufficient calibration images.")


# Undistortion function
def undistort_image(frame):
    h, w = frame.shape[:2]  # Get the height and width of the image

    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w, h), 1, frameSize)

    # Undistort
    dst = cv.undistort(frame, cameraMatrix, distCoeffs, None, newCameraMatrix)

    # Resize the frame to the original size
    resized_frame = cv.resize(dst, (w, h))

    # Crop the image
    x, y, w, h = roi
    dst = resized_frame[y:y + h, x:x + w]
    return dst


# Continuous undistortion function
def continuous_undistortion(image):
    undistorted_image = undistort_image(image)

    return undistorted_image
