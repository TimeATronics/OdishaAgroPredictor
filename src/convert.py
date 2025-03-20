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
import pandas as pd
import os

years = list(range(2010, 2020))
districts = [
    "ANGUL", "BALASORE", "BARGARH", "BHADRAK", "BOLANGIR", "BOUDH", "CUTTACK", "DEOGARH",
    "DHENKANAL", "GAJAPATI", "GANJAM", "JAGATSINGHPUR", "JAJPUR", "JHARSUGUDA", "KALAHANDI",
    "KANDHAMAL", "KENDRAPARA", "KEONJHAR", "KHORDHA", "KORAPUT", "MALKANGIRI", "MAYURBHANJ",
    "NABARANGPUR", "NAYAGARH", "NUAPADA", "PURI", "RAYAGADA", "SAMBALPUR", "SUBARNAPUR", "SUNDARGARH"
]

district_data = {district: [] for district in districts}

for year in years:
    filename = f"crops_{year}.csv"
    
    if not os.path.exists(filename):
        print(f"File {filename} not found. Skipping...")
        continue
    
    df = pd.read_csv(filename)
    df.insert(0, "Year", year)
    
    for district in districts:
        district_row = df[df["district"] == district]
        if not district_row.empty:
            district_row = district_row.drop(columns=["district"])
            district_data[district].append(district_row.iloc[0])

for district, records in district_data.items():
    if records:
        district_df = pd.DataFrame(records)
        output_filename = f"dist_{district}.csv"
        district_df.to_csv(output_filename, index=False)
        print(f"Saved {output_filename}")
    else:
        print(f"No data found for {district}, skipping file creation.")