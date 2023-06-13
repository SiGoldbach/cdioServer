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

def un_distort(frame):
    h, w = frame.shape[:2]
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, frameSize)

    # Undistort
    dst = cv.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)

    # Crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    dst = cv.resize(dst, frameSize)

    cv.imwrite('caliResult1.jpg', dst)

    # Un distort with Remapping
    mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w, h),
                                            cv.CV_32FC1)  # Use cv.CV_32FC1 for better precision
    dst = cv.remap(frame, mapx, mapy, cv.INTER_LINEAR)

    # Crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    dst = cv.resize(dst, frameSize)

    cv.imwrite('caliResult2.jpg', dst)

    # Reprojection Error
    mean_error = 0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        mean_error += error

    print("total error: {}".format(mean_error / len(objpoints)))
    return dst

# Perform calibration
un_distort(cv.imread('calibration_images/calibration_photo_1.jpg'))

################ CONTINUOUS UNDISTORTION ########################################

def continuous_undistortion():
    video = cv.VideoCapture(1, cv.CAP_DSHOW)  # Use 0 or the appropriate camera index

    video.set(cv.CAP_PROP_FRAME_WIDTH, frameSize[0])
    video.set(cv.CAP_PROP_FRAME_HEIGHT, frameSize[1])

    while True:
        ret, frame = video.read()

        if ret:
            undistorted_frame = un_distort(frame)

            cv.imshow('Undistorted Image', undistorted_frame)

        if cv.waitKey(1) == ord('q'):
            break

    video.release()
    cv.destroyAllWindows()

# Start continuous undistortion
continuous_undistortion()
