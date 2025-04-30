import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Load and resize images
image1 = cv2.imread('image1.png')
image2 = cv2.imread('image2.png')
image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

# Convert to grayscale
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Calculate SSIM
score, diff = ssim(gray1, gray2, full=True)
diff = (diff * 255).astype("uint8")
print(f"SSIM Score: {score:.4f}")

# Threshold to find regions with differences
_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY_INV)

# Find contours of the differences
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
image_diff = image2.copy()
for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(image_diff, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Show results
cv2.imshow("Image1", image1)
cv2.imshow("Image2", image2)
cv2.imshow("SSIM Diff", diff)
cv2.imshow("Highlighted Differences", image_diff)
cv2.waitKey(0)
cv2.destroyAllWindows()
