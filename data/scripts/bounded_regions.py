import cv2
import numpy as np

# Load the map image
image = cv2.imread("../inputs/map_image.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate over the contours and draw bounding rectangles
regions = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    regions.append((x, y, x + w, y + h))

# Display the extracted regions
for region in regions:
    x1, y1, x2, y2 = region
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Show the image with regions
cv2.imshow("Extracted Regions", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

