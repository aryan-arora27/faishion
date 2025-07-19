# backend/main.py

from models import apparel_detector, color_extractor
from models.color_extractor import extract_top_colors
from models.recommender_model import DualOutfitRecommender

img_path = "test_images/t1.jpeg"
skin_color = "fair"  

apparel_type, cropped_image = apparel_detector.detect(img_path)

if apparel_type is None:
    print("[MAIN] No apparel detected.")
    exit()

top_items = ["shirt", "tshirt", "hoodie", "dress"]
bottom_items = ["jeans", "trousers", "shorts", "shoes"]

if apparel_type in top_items:
    top_colors = extract_top_colors(cropped_image,top_or_bottom="top")
else:
    top_colors=extract_top_colors(cropped_image,top_or_bottom="bottom")

print("Top Colors:", top_colors)
print(f"Apparel: {apparel_type}, Dominant Colors: {top_colors}")
cropped_image.show()  

recommender = DualOutfitRecommender.load_model("data/recommender_dual.pkl")



if apparel_type in top_items:
    suggestions = recommender.recommend(
        top_type=apparel_type,
        top_colors=top_colors,
        skin_color=skin_color
    )
    print("\nOutfit Suggestions (based on top):")
    for i, s in enumerate(suggestions, 1):
        print(f"{i}. Pair your {s['source_color']} {apparel_type} with {s['match_color']} {s['match_type']}")

elif apparel_type in bottom_items:
    suggestions = recommender.recommend(
        bottom_type=apparel_type,
        bottom_color=top_colors[0],  # Use only 1st color for bottom
        skin_color=skin_color
    )
    print("\nOutfit Suggestions (based on bottom):")
    for i, s in enumerate(suggestions, 1):
        print(f"{i}. Pair your {top_colors[0]} {apparel_type} with a {s['match_color']} {s['match_type']}")

else:
    print(f"[MAIN] Apparel type '{apparel_type}' is not recognized for recommendation.")
