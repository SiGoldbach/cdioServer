import numpy as np
import cv2
import glob

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

    # Print the obtained camera matrix and distortion coefficients
    print("Camera Matrix:")
    print(camera_matrix)
    print("\nDistortion Coefficients:")
    print(distortion_coeffs)
else:
    print("Insufficient data for calibration. Check if the corners were detected in any image.")
