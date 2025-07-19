from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
TOP_COLORS = ['beige', 'black', 'blue', 'brown', 'cream', 'green', 'grey', 'lavender',
              'light blue', 'maroon', 'navy', 'olive', 'peach', 'pink', 'red', 'teal', 'white', 'yellow']

BOTTOM_COLORS = ['beige', 'black', 'blue', 'brown', 'cream', 'dark blue', 'denim',
                 'grey', 'khakhi', 'navy', 'olive', 'tan', 'white']

PREDEFINED_RGB = {
    'beige': (237, 232, 208),
    'black': (0, 0, 0),
    'blue': (0, 0, 255),
    'brown': (137, 81, 41),
    'cream': (253, 251, 212),
    'green': (0, 128, 0),
    'grey': (137, 137, 137),
    'lavender': (211, 211, 255),
    'light blue': (144, 213, 255),
    'maroon': (85, 0, 0),
    'navy': (0, 0, 128),
    'olive': (99, 107, 47),
    'peach': (255, 211, 172),
    'pink': (255, 141, 161),
    'red': (255, 44, 44),
    'teal': (6, 148, 148),
    'white': (255, 255, 255),
    'yellow': (255, 222, 33),
    'dark blue': (17, 17, 132),
    'denim': (21, 96, 189),
    'khakhi': (213, 197, 138),
    'tan': (214, 181, 136)
}

def extract_top_colors(image: Image.Image, k=3, top_or_bottom='top'):
    image = image.resize((100, 100))
    img_array = np.array(image)
    img_array = img_array.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k, random_state=42).fit(img_array)
    cluster_centers = kmeans.cluster_centers_.astype(int)

    allowed_colors = TOP_COLORS if top_or_bottom == 'top' else BOTTOM_COLORS

    def closest_allowed_color(rgb):
        min_dist = float('inf')
        closest_name = None
        for name in allowed_colors:
            ref_rgb = PREDEFINED_RGB[name]
            dist = np.sum((np.array(rgb) - np.array(ref_rgb))**2)
            if dist < min_dist:
                min_dist = dist
                closest_name = name
        return closest_name

    unique_colors = []
    for center in cluster_centers:
        name = closest_allowed_color(center)
        if name not in unique_colors:
            unique_colors.append(name)
        if len(unique_colors) == 2:
            break

    print(f"[COLOR EXTRACTOR] Top colors: {unique_colors}")
    return unique_colors
