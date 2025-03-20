""" 
 * This file is part of the OdishaAgroPredictor distribution (https://github.com/TimeATronics/OdishaAgroPredictor).
 * Copyright (c) 2025 Aradhya Chakrabarti
 * 
 * This program is free software: you can redistribute it and/or modify  
 * it under the terms of the GNU General Public License as published by  
 * the Free Software Foundation, version 3.
 *
 * This program is distributed in the hope that it will be useful, but 
 * WITHOUT ANY WARRANTY; without even the implied warranty of 
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License 
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
import branca
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class MapViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Odisha Yield Prediction Maps")
        self.setGeometry(100, 100, 1024, 768)

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        self.load_page("index.html")

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Options")

        back_action = QAction("Back to Home", self)
        back_action.triggered.connect(lambda: self.load_page("index.html"))
        file_menu.addAction(back_action)

    def load_page(self, file_name):
        abs_path = os.path.abspath(file_name)
        print(f"Loading: {abs_path}")

        if os.path.exists(abs_path):
            self.web_view.setUrl(QUrl.fromLocalFile(abs_path))
        else:
            print("Error: File not found!", abs_path)

kml_file = "odisha.kml"
odisha_map = gpd.read_file(kml_file, driver="KML")
odisha_map.rename(columns={"Name": "district"}, inplace=True)
odisha_map["district"] = odisha_map["district"].str.upper()

district_mapping = {
    "BALASORE (BALESHWAR)": "BALASORE", "BARAGARH": "BARGARH", "KENDRAPARHA": "KENDRAPARA", "KEONJHAR (KENDUJHAR)": "KEONJHAR",
    "BOLANGIR (BALANGIR)": "BOLANGIR", "JAJAPUR": "JAJPUR", "KENDUJHAR": "KEONJHAR", "BAUDH (BAUDA)": "BOUDH",
    "ANUGUL": "ANGUL", "NABARANGAPUR": "NABARANGPUR", "NUAPARHA": "NUAPADA", "RAYAGARHA": "RAYAGADA"
}
odisha_map["district"] = odisha_map["district"].replace(district_mapping)
districts = odisha_map["district"].tolist()

features = ["rice_area_kharif", "rice_area_rabi", "cereals_area_kharif", "cereals_area_rabi",
            "grain_area_kharif", "grain_area_rabi", "intensity", "rain_kharif", "rain_rabi",
            "Mean_Temp_Kharif", "Mean_Temp_Rabi", "calamity_severity"]

targets = {
    "rice": ["rice_yield_kharif", "rice_yield_rabi"],
    "cereals": ["cereals_yield_kharif", "cereals_yield_rabi"],
    "grain": ["grain_yield_kharif", "grain_yield_rabi"]
}

predictions_2026 = {"rice": {}, "cereals": {}, "grain": {}}
metrics_data = []

for district in districts:
    corrected_district = district_mapping.get(district, district)
    file_path = f"data/dist_{corrected_district}.csv"
    
    if not os.path.exists(file_path):
        print(f"Skipping {district} (No Data Found): Expected file - {file_path}")
        continue

    df = pd.read_csv(file_path)
    X = df[features]

    for crop, target_cols in targets.items():
        Y = df[target_cols]
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        
        model = LinearRegression()
        model.fit(X_train, Y_train)

        Y_pred = model.predict(X_test)
        mae = mean_absolute_error(Y_test, Y_pred)
        mse = mean_squared_error(Y_test, Y_pred)
        r2 = r2_score(Y_test, Y_pred)
        adj_r2 = 1 - (1 - r2) * ((len(Y_test) - 1) / (len(Y_test) - X_test.shape[1] - 1))
        
        metrics_data.append([district, crop, mae, mse, r2, adj_r2])

        future_data = pd.DataFrame({col: [df[col].mean() * np.random.uniform(0.9, 1.1)] for col in features})
        future_data["calamity_severity"] = [0]
        future_yield = model.predict(future_data)        
        predictions_2026[crop][district] = np.maximum(0, future_yield.flatten())

        print(f"\nGenerated Inputs for 2026 ({district} - {crop}):")
        print(future_data.to_string(index=False))

pred_dfs = {crop: pd.DataFrame.from_dict(pred, orient="index", columns=targets[crop]) for crop, pred in predictions_2026.items()}
for crop, df in pred_dfs.items():
    df["total_production"] = df.sum(axis=1)
    odisha_map = odisha_map.merge(df, left_on="district", right_index=True, how="left")

metrics_df = pd.DataFrame(metrics_data, columns=["District", "Crop", "MAE", "MSE", "R²", "Adjusted R²"])
print("\nModel Performance Metrics:")
print(metrics_df.to_string(index=False))

def create_map(crop, title, file_name):
    m = folium.Map(location=[20.5, 84.5], zoom_start=6, tiles="cartodbpositron")
    colormap = branca.colormap.linear.Blues_09.scale(
        odisha_map["total_production"].min(), odisha_map["total_production"].max()
    ).to_step(10)
    colormap.caption = title
    
    def style_function(feature):
        district_name = feature["properties"]["district"]
        production_value = pred_dfs[crop].loc[district_name, "total_production"] if district_name in pred_dfs[crop].index else None
        color = colormap(production_value) if production_value else "#d3d3d3"
        return {"fillColor": color, "color": "black", "weight": 0.5, "fillOpacity": 0.7}

    folium.GeoJson(
        odisha_map, style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=["district", "total_production"])
    ).add_to(m)
    colormap.add_to(m)
    m.save(file_name)

display_titles = {"rice": "Rice Yield Prediction (kg/ha)", "cereals": "Cereals Yield Prediction (kg/ha)", "grain": "Grain Yield Prediction (kg/ha)"}
file_names = {"rice": "rice_yield_map.html", "cereals": "cereals_yield_map.html", "grain": "grain_yield_map.html"}

for crop in targets.keys():
    create_map(crop, display_titles[crop], file_names[crop])

plt.figure(figsize=(12, 6))
for crop, df in pred_dfs.items():
    sorted_df = df.sort_values("total_production", ascending=False)
    sns.barplot(x=sorted_df.index, y=sorted_df["total_production"], label=display_titles[crop])

plt.xticks(rotation=90)
plt.xlabel("District")
plt.ylabel("Predicted Total Production (kg/ha)")
plt.title("Predicted Crop Production by District for 2026")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
for crop, df in pred_dfs.items():
    for district in df.index:
        actual_values = df.loc[district, targets[crop]].values
        predicted_value = df.loc[district, "total_production"]
        residuals = actual_values - predicted_value
        plt.scatter(actual_values, residuals, label=district, alpha=0.6)

plt.axhline(y=0, color="red", linestyle="--")
plt.xlabel("Actual Values (10 years)")
plt.ylabel("Residuals (Actual - Predicted)")
plt.title("Residual Plot for Predicted Yield")
plt.grid()
plt.show(block=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec_())