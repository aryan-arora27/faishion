from models.recommender_model import DualOutfitRecommender

model = DualOutfitRecommender()
model.load_and_train("data/fashion_outfits_with_skin_color.csv")
model.save_model("data/recommender_dual.pkl")

print("[TRAINING] Recommender model trained and saved.")
