import numpy as np
import cv2
import glob

def perform_calibration():
    # Define the calibration pattern size (number of inner corners)
    pattern_size = (12, 8)  # Width, height

    # Prepare arrays to store object points and image points from calibration images
    object_points = []  # 3D coordinates of calibration pattern corners
    image_points = []  # 2D coordinates of detected corners in images

    # Generate coordinates of calibration pattern corners
    object_points_pattern = np.zeros((np.prod(pattern_size), 3), dtype=np.float32)
    object_points_pattern[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)

    # Capture calibration images
    calibration_images = glob.glob("calibration_images/*.jpg")  # Adjust the path and image format as per your images

    for image_path in calibration_images:
        # Load the image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        if ret:
            object_points.append(object_points_pattern)
            image_points.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(image, pattern_size, corners, ret)
            cv2.imshow("Chessboard Corners", image)
            cv2.waitKey(500)  # Adjust the wait time as needed
        else:
            print("Corners not found in image:", image_path)

    cv2.destroyAllWindows()

    # Perform camera calibration
    image_size = gray.shape[::-1]  # Image size should be the same for all calibration images

    if len(object_points) > 0 and len(image_points) > 0:
        _, camera_matrix, distortion_coeffs, _, _ = cv2.calibrateCamera(
            object_points, image_points, image_size, None, None
        )

        # Save the camera matrix and distortion coefficients to a file for later use
        np.savez('calibration_data.npz', camera_matrix=camera_matrix, distortion_coeffs=distortion_coeffs)

        return camera_matrix, distortion_coeffs

    else:
        print("Insufficient data for calibration. Check if the corners were detected in any image.")
        return None, None


def undistort_image(image_path, camera_matrix, distortion_coeffs):
    # Load the image for undistortion
    image = cv2.imread(image_path)

    if image is not None:
        # Undistort the image
        undistorted_image = cv2.undistort(image, camera_matrix, distortion_coeffs)

        # Calculate the mapx and mapy for remapping
        h, w = image.shape[:2]
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coeffs, (w, h), 1, (w, h))
        mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, distortion_coeffs, None, new_camera_matrix, (w, h), 5)

        # Apply remapping to adjust parts of the image
        output_image = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)

        # Crop the image
        x, y, width, height = roi
        output_image = output_image[y:y + height, x:x + width]

        # Save the undistorted image
        cv2.imwrite('undistorted_image.jpg', output_image)

    else:
        print("Failed to load the image:", image_path)


# Perform camera calibration and obtain the camera matrix and distortion coefficients
camera_matrix, distortion_coeffs = perform_calibration()

# Load the calibration parameters (camera matrix and distortion coefficients) from the calibration_data.npz file
if camera_matrix is not None and distortion_coeffs is not None:
    # Use the camera matrix and distortion coefficients for image undistortion
    undistort_image('../Resources/Pictures/calibration_photo_1.jpg', camera_matrix, distortion_coeffs)
