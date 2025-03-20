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
import numpy as np
import pandas as pd

lats = np.arange(7.5, 38.5, 1.0)
lons = np.arange(67.5, 98.5, 1.0)

district_coords = {
    "ANGUL": (21.0, 86.5),
    "BALASORE": (21.5, 87.0),
    "BARGARH": (21.0, 83.5),
    "BHADRAK": (21.0, 86.5),
    "BOLANGIR": (20.5, 83.5),
    "BOUDH": (20.5, 84.5),
    "CUTTACK": (20.5, 86.0),
    "DEOGARH": (21.5, 84.5),
    "DHENKANAL": (21.0, 85.5),
    "GAJAPATI": (19.0, 84.0),
    "GANJAM": (19.5, 85.0),
    "JAGATSINGHPUR": (20.5, 86.5),
    "JAJPUR": (21.0, 86.5),
    "JHARSUGUDA": (21.5, 84.0),
    "KALAHANDI": (20.0, 83.0),
    "KANDHAMAL": (20.5, 84.0),
    "KENDRAPARA": (20.5, 86.5),
    "KEONJHAR": (22.0, 86.0),
    "KHORDHA": (20.0, 85.5),
    "KORAPUT": (19.0, 82.5),
    "MALKANGIRI": (18.5, 82.0),
    "MAYURBHANJ": (22.0, 86.5),
    "NABARANGPUR": (19.5, 82.5),
    "NAYAGARH": (20.0, 85.0),
    "NUAPADA": (20.0, 82.5),
    "PURI": (19.5, 85.5),
    "RAYAGADA": (19.0, 83.5),
    "SAMBALPUR": (21.5, 84.0),
    "SUBARNAPUR": (20.5, 84.0),
    "SUNDARGARH": (22.0, 84.0)
}

def find_nearest_grid(lat, lon):
    lat_idx = np.argmin(np.abs(lats - lat))
    lon_idx = np.argmin(np.abs(lons - lon))
    return lat_idx, lon_idx

district_grid_indices = {d: find_nearest_grid(*coords) for d, coords in district_coords.items()}

def read_grd_file(filename):
    with open(filename, "rb") as f:
        data = np.fromfile(f, dtype=np.float32)
    return data.reshape(-1, 31, 31)

def process_temperature(grd_filename):
    temp_data = read_grd_file(grd_filename)
    num_days = temp_data.shape[0]
    
    kharif_months = list(range(151, 304))
    rabi_months = list(range(304, 365)) + list(range(0, 90))

    results = []
    
    for district, (lat_idx, lon_idx) in district_grid_indices.items():
        kharif_temps = temp_data[kharif_months, lat_idx, lon_idx]
        rabi_temps = temp_data[rabi_months, lat_idx, lon_idx]
        
        mean_kharif = round(np.nanmean(kharif_temps), 2)
        mean_rabi = round(np.nanmean(rabi_temps), 2)
        
        results.append([district, mean_kharif, mean_rabi])
    
    df = pd.DataFrame(results, columns=["District", "Mean_Temp_Kharif", "Mean_Temp_Rabi"])
    return df

grd_file = "C:\\Users\\AradhyaPC\\Downloads\\Maxtemp_MaxT_2010.GRD"
df = process_temperature(grd_file)
df.to_csv("temp_2010.csv", index=False)
