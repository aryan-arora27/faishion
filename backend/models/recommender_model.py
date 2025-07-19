import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class DualOutfitRecommender:
    def __init__(self):
        self.top_type_enc = LabelEncoder()
        self.top_color_enc = LabelEncoder()
        self.bottom_type_enc = LabelEncoder()
        self.bottom_color_enc = LabelEncoder()
        self.skin_color_enc = LabelEncoder()
        self.output_enc_top = LabelEncoder()
        self.output_enc_bottom = LabelEncoder()

        self.model_top_to_bottom = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model_bottom_to_top = RandomForestClassifier(n_estimators=100, random_state=42)

    def load_and_train(self, csv_path="../data/fashion_outfits_with_skin_color.csv"):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"{csv_path} not found.")

        df = pd.read_csv(csv_path)
        all_skin_tones =["light", "medium", "dark","brown","fair","olive","tan"]

        any_rows = df[df["skin_color"] == "any"]
        expanded_rows = []

        for tone in all_skin_tones:
            clone = any_rows.copy()
            clone["skin_color"] = tone
            expanded_rows.append(clone)

        df = df[df["skin_color"] != "any"]  
        if expanded_rows:
            df = pd.concat([df] + expanded_rows, ignore_index=True)

        X_tb = pd.DataFrame({
            'top_type': self.top_type_enc.fit_transform(df['top_type']),
            'top_color': self.top_color_enc.fit_transform(df['top_color']),
            'skin_color': self.skin_color_enc.fit_transform(df['skin_color'])
        })

        y_tb_raw = df['bottom_type'] + "_" + df['bottom_color']
        y_tb = self.output_enc_bottom.fit_transform(y_tb_raw)
        self.model_top_to_bottom.fit(X_tb, y_tb)

        X_bt = pd.DataFrame({
            'bottom_type': self.bottom_type_enc.fit_transform(df['bottom_type']),
            'bottom_color': self.bottom_color_enc.fit_transform(df['bottom_color']),
            'skin_color': self.skin_color_enc.transform(df['skin_color'])
        })

        y_bt_raw = df['top_type'] + "_" + df['top_color']
        y_bt = self.output_enc_top.fit_transform(y_bt_raw)
        self.model_bottom_to_top.fit(X_bt, y_bt)

        print("[RECOMMENDER] Models trained successfully (with 'any' skin color expansion).")

        
    def recommend(self, *, top_type=None, top_colors=None, bottom_type=None, bottom_color=None, skin_color="any"):
        if top_type and top_colors:
            color1, color2 = top_colors[0], top_colors[1] if len(top_colors) > 1 else top_colors[0]
            suggestions = []

            try:
                x1 = pd.DataFrame([{
                    'top_type': self.top_type_enc.transform([top_type])[0],
                    'top_color': self.top_color_enc.transform([color1])[0],
                    'skin_color': self.skin_color_enc.transform([skin_color])[0]
                }])
                probs1 = self.model_top_to_bottom.predict_proba(x1)[0]
                top2_indices = probs1.argsort()[::-1][:2]
                preds1 = self.output_enc_bottom.inverse_transform(top2_indices)
                for pred in preds1:
                    bottom_type, bottom_color = pred.split("_")
                    suggestions.append({
                        "match_type": bottom_type,
                        "match_color": bottom_color,
                        "source_color": color1
                    })
            except ValueError as e:
                print("[RECOMMENDER] Error with first color:", e)

            try:
                x2 = pd.DataFrame([{
                    'top_type': self.top_type_enc.transform([top_type])[0],
                    'top_color': self.top_color_enc.transform([color2])[0],
                    'skin_color': self.skin_color_enc.transform([skin_color])[0]
                }])
                probs2 = self.model_top_to_bottom.predict_proba(x2)[0]
                top1_index = probs2.argsort()[::-1][0]
                pred2 = self.output_enc_bottom.inverse_transform([top1_index])[0]
                bottom_type, bottom_color = pred2.split("_")
                suggestions.append({
                    "match_type": bottom_type,
                    "match_color": bottom_color,
                    "source_color": color2
                })
            except ValueError as e:
                print("[RECOMMENDER] Error with second color:", e)

            return suggestions

        elif bottom_type and bottom_color:
            try:
                x = pd.DataFrame([{
                    'bottom_type': self.bottom_type_enc.transform([bottom_type])[0],
                    'bottom_color': self.bottom_color_enc.transform([bottom_color])[0],
                    'skin_color': self.skin_color_enc.transform([skin_color])[0]
                }])
                probs = self.model_bottom_to_top.predict_proba(x)[0]
                top_indices = probs.argsort()[::-1][:3]
                preds = self.output_enc_top.inverse_transform(top_indices)
                return [
                    {"match_type": t.split("_")[0], "match_color": t.split("_")[1]}
                    for t in preds
                ]
            except ValueError as e:
                print("[RECOMMENDER] Error (bottom-to-top):", e)
                return []

        else:
            raise ValueError("Invalid input: Provide either (top_type + top_colors) or (bottom_type + bottom_color)")

    def save_model(self, path="data/recommender_dual.pkl"):
        joblib.dump(self, path)

    @staticmethod
    def load_model(path="data/recommender_dual.pkl"):
        return joblib.load(path)
