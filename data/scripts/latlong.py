import numpy as np

def interpolate_lat_longs(image_size):
    # Define the latitude and longitude coordinates of the corners of Colorado
    lat_top_left, lon_top_left = 41.003444, -109.045223  # Northwest corner
    lat_top_right, lon_top_right = 41.003444, -102.041524  # Northeast corner
    lat_bottom_left, lon_bottom_left = 36.993083, -109.045223  # Southwest corner

    # Calculate the latitude and longitude intervals between corners
    lat_interval = (lat_bottom_left - lat_top_left) / (image_size[0] - 1)
    lon_interval = (lon_top_right - lon_top_left) / (image_size[1] - 1)

    # Create an empty array to store the latitude and longitude values
    lat_longs = np.empty(image_size, dtype=object)

    # Iterate over each pixel and calculate the latitude and longitude
    for i in range(image_size[0]):
        for j in range(image_size[1]):
            # Calculate the latitude and longitude for the current pixel
            lat = lat_top_left + i * lat_interval
            lon = lon_top_left + j * lon_interval

            # Store the latitude and longitude in the array
            lat_longs[i, j] = (lat, lon)

    return lat_longs

# Define the size of the image (number of rows and columns)
image_size = (1000, 1000)

# Call the function to interpolate the latitude and longitude values
lat_longs = interpolate_lat_longs(image_size)

# Access the latitude and longitude of a specific pixel
row = 500
col = 700
lat, lon = lat_longs[row, col]

# Print the latitude and longitude of the pixel
print(f"Latitude: {lat:.6f}")
print(f"Longitude: {lon:.6f}")
