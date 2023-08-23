from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

def create_image_with_pixels(array_size, pixel_set):
    # Create a new blank image with the specified size
    image = Image.new("L", array_size, color=255)
    
    # Create a draw object
    draw = ImageDraw.Draw(image)
    
    # Iterate over the set of pixels
    for pixel in pixel_set:
        # Set the pixel to black (0)
        draw.point(pixel, fill=0)
    
    return image


def find_self_contained_regions(array, min_region_size):
    rows, cols = array.shape
    grid = np.zeros((rows, cols), dtype=int)
    regions = []
    region_counter = 1
    region_sizes = {}
    
    def get_neighbors(row, col):
        neighbors = []
        if row > 0:
            neighbors.append((row-1, col))  # Up
        if row < rows - 1:
            neighbors.append((row+1, col))  # Down
        if col > 0:
            neighbors.append((row, col-1))  # Left
        if col < cols - 1:
            neighbors.append((row, col+1))  # Right
        return neighbors
    
    def flood_fill(start_row, start_col, region):
        stack = [(start_row, start_col)]
        size = 0
        while stack:
            row, col = stack.pop()
            if grid[row, col] == 0 and array[row, col] == 0:
                grid[row, col] = region
                size += 1
                neighbors = get_neighbors(row, col)
                stack.extend(neighbors)
        return size
    
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 0 and array[i, j] == 0:
                size = flood_fill(i, j, region_counter)
                if size >= min_region_size:
                    regions.append(region_counter)
                    region_sizes[region_counter] = size
                    region_counter += 1
    
    return grid, regions, region_sizes
 
def group_pixels(image_path):
    # Load the image
    image = Image.open(image_path)

    # Convert the image to RGB mode (3 channels)
    image = image.convert("RGB")

    # Convert the image to a numpy array
    pixels = np.array(image)

    # Reshape the array to a 2D matrix of pixels
    reshaped_pixels = pixels.reshape(-1, 3)

    # Group the pixels based on their color using K-means clustering
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=7, random_state=42)
    labels = kmeans.fit_predict(reshaped_pixels)

    # Create a dictionary to store the color groups
    color_groups = {i: [] for i in range(7)}

    # Iterate over each pixel and assign its index to the corresponding color group
    for i, label in enumerate(labels):
        color_groups[label].append(i)

    # Find the groups that have different values for each channel
    groups_with_different_channels = []
    for i, pixel_indices in color_groups.items():
        if len(pixel_indices) > 0:
            pixels_in_group = reshaped_pixels[pixel_indices]
            unique_channel_values = np.unique(pixels_in_group, axis=0)
            if len(unique_channel_values) > 1:
                groups_with_different_channels.append(i)

    # Create a new image with colored pixels representing each group
    output_image = np.zeros_like(pixels)
    group_colors = [
        [255, 0, 0],    # Red
        [0, 255, 0],    # Green
        [0, 0, 255],    # Blue
        [255, 255, 0],  # Yellow
        [255, 0, 255],  # Magenta
        [0, 255, 255],  # Cyan
        [255, 128, 0]   # Orange
    ]
    for group_id, pixel_indices in color_groups.items():
        group_color = group_colors[group_id % len(group_colors)]
        output_image[np.unravel_index(pixel_indices, pixels.shape[:2])] = group_color

    # Convert the numpy array back to PIL image
    output_image = Image.fromarray(output_image)

    # Display the output image
    output_image.show()

    return color_groups

# Provide the path to the image file
image_path = '../inputs/colorado.png'
image = Image.open(image_path)
image = image.convert("RGB")
pixels = np.array(image)

# Call the function to group pixels and generate an image with colored pixels representing each group
color_groups = group_pixels(image_path)

output_image = np.zeros((pixels.shape[0], pixels.shape[1]))
output_image[np.unravel_index(color_groups[2], pixels.shape[:2])] = 1
grid, regions, region_sizes = find_self_contained_regions(output_image,20)

num_regions = len(regions)
colors = plt.cm.tab20b(np.linspace(0, 1, num_regions + 1))  # Add one more color for the background
image = colors[grid]

plt.imshow(image)
plt.axis('off')
plt.show()

plt.ion()

# Get mouse clicks
points = []
while True:
    click = plt.ginput(n=1, timeout=0)
    if not click:
        break
    points.append(click[0])

# Disable interactive mode
plt.ioff()

# Close the figure
plt.close()

# Save pixel coordinates to a text file
file_path = 'group_pixel_locations.txt'
with open(file_path, 'w') as f:
    for i, point in enumerate(points):
        x, y = point
        f.write(f"Clicked pixel {i + 1}: x={x}, y={y}\n")

print(f"Pixel locations saved to {file_path}")

for region in regions:
    size = region_sizes[region]
    print(f"Region {region}: Size {size}")
