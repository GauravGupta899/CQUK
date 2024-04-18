from time import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import shuffle
from matplotlib.image import imread
import cv2
import os

class ImageQuantizer:
    def __init__(self, n_colors=64, image_path=""):
        self.n_colors = n_colors
        self.kmeans = None
        self.codebook_random = None
        self.labels = None
        self.labels_random = None
        self.save_folder = "static/generated/"
        self.original = os.path.basename(image_path)

    def fit(self, image):
        # Convert image to floats
        image = np.array(image, dtype=np.float64) / 255

        # Reshape image to 2D array
        w, h, d = original_shape = tuple(image.shape)
        assert d == 3
        image_array = np.reshape(image, (w * h, d))

        # Fit KMeans on a small sub-sample of the data
        image_array_sample = shuffle(image_array, random_state=0, n_samples=1000)
        self.kmeans = KMeans(n_clusters=self.n_colors, random_state=0).fit(image_array_sample)

        # Get labels for all points
        self.labels = self.kmeans.predict(image_array)

        # Create random codebook
        self.codebook_random = shuffle(image_array, random_state=0, n_samples=self.n_colors)
        self.labels_random = pairwise_distances_argmin(self.codebook_random, image_array, axis=0)

    def recreate_image(self, codebook, labels, w, h):
        """Recreate the (compressed) image from the code book & labels"""
        return codebook[labels].reshape(w, h, -1)

    def save_results(self, original_image):
        w, h, _ = original_image.shape

        # # Display original image
        # plt.figure()
        # plt.axis("off")
        # plt.title("Original image")
        # plt.imshow(original_image)

        # Display quantized image using K-Means
        # plt.figure()
        # plt.axis("off")
        # plt.title(f"Quantized image ({self.n_colors} colors, K-Means)")
        quantized_image_kmeans = self.recreate_image(self.kmeans.cluster_centers_, self.labels, w, h)
        # plt.imshow(quantized_image_kmeans)
        # # save image 
        plt.imsave(self.save_folder+self.original, quantized_image_kmeans)

        return self.save_folder+self.original

       
# Example usage
if __name__ == "__main__":
    # Load the image using matplotlib
    image_path = r"C:\Users\gaura\Documents\CQUK\static\uploads\modi.jpg"  # Change this to your image path
    custom_image = imread(image_path)
    # Create ImageQuantizer object
    quantizer = ImageQuantizer(n_colors=64, image_path=image_path)
    # Fit the quantizer with the custom image
    quantizer.fit(custom_image)
    # Plot the results
    output = quantizer.save_results(custom_image)
    print(output)