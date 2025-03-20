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

data_2017 = {
    "District": [
        "Angul", "Balasore", "Baragarh", "Bhadrak", "Bolangir", "Boudh", "Cuttack", "Deogarh", "Dhenkanal",
        "Gajapati", "Ganjam", "Jagatsinghpur", "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapada",
        "Keonjhar", "Khordha", "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur", "Nayagarh", "Nuapada",
        "Puri", "Rayagada", "Sambalpur", "Subarnapur", "Sundargarh"
    ],
    "Jan": [8.4, 0, 7.0, 32.9, 3.5, 0, 0, 8.1, 0, 0, 0, 42.8, 7.9, 7.5, 15.5, 0, 0, 0.9, 0.7, 10.7, 0, 2.7, 0, 0.3, 0, 0, 3.9, 17.4, 0, 3.3],
    "Feb": [22.4, 105.3, 11.8, 19.0, 1.3, 3.7, 0, 4.1, 0, 81.4, 0, 0, 0, 4.6, 15.5, 0, 81.5, 35.4, 52.7, 74.5, 0, 44.9, 13.5, 59.6, 0, 22.7, 5.1, 0, 0, 0],
    "Mar": [1.2, 18.5, 7.0, 10.7, 13.3, 3.7, 6.3, 0.3, 9.4, 2.4, 49.3, 0, 0, 1.6, 2.6, 6.7, 0, 11.5, 17.6, 13.6, 16.5, 32.3, 15.1, 8.4, 8.7, 5.3, 33.5, 3.5, 0, 0.4],
    "Apr": [35.8, 166.0, 4.8, 44.9, 23.8, 16.3, 15.9, 27.2, 12.4, 109.7, 40.8, 14.8, 86.7, 0.4, 209.4, 238.8, 14.2, 117.6, 164.9, 76.8, 39.3, 139.3, 57.5, 132.9, 0, 105.8, 70.3, 33.4, 46.8, 46.8],
    "May": [201.1, 318.0, 219.0, 196.9, 187.8, 322.6, 161.8, 449.4, 126.4, 345.9, 212.7, 375.4, 227.9, 442.3, 511.9, 211.6, 216.5, 320.5, 402.2, 380.8, 385.3, 139.3, 470.4, 317.4, 144.8, 110.6, 267.5, 272.4, 260.1, 260.1],
    "Jun": [213.4, 276.5, 234.2, 275.4, 238.1, 282.0, 207.1, 385.2, 197.0, 463.2, 296.8, 346.5, 235.9, 308.8, 342.7, 246.4, 510.5, 230.3, 313.2, 382.1, 291.0, 385.3, 448.3, 254.8, 224.2, 314.4, 239.2, 256.8, 306.7, 306.7],
    "Jul": [213.1, 198.0, 202.1, 215.4, 206.8, 192.0, 224.6, 224.9, 200.9, 200.9, 264.1, 300.0, 363.2, 245.8, 308.9, 216.4, 517.3, 230.5, 239.1, 175.5, 170.1, 291.0, 152.0, 183.1, 183.1, 192.1, 181.7, 201.6, 201.6, 201.6],
    "Aug": [143.7, 251.6, 163.2, 120.9, 132.7, 152.9, 193.5, 136.2, 185.5, 200.9, 180.4, 327.9, 190.7, 97.1, 196.7, 195.4, 147.9, 166.2, 249.3, 174.5, 189.1, 189.1, 152.0, 181.7, 181.7, 192.1, 178.7, 62.2, 201.6, 201.6],
    "Sep": [109.1, 47.2, 56.6, 242.0, 59.6, 202.2, 222.4, 95.4, 167.8, 200.9, 209.3, 130.5, 97.1, 97.1, 195.4, 195.4, 125.5, 160.3, 249.3, 174.5, 170.1, 189.1, 152.0, 181.7, 181.7, 192.1, 178.7, 62.2, 201.6, 201.6],
    "Oct": [16.9, 47.2, 65.7, 76.5, 59.6, 152.9, 63.8, 167.8, 70.7, 200.9, 76.2, 130.5, 74.3, 97.1, 195.4, 195.4, 125.5, 160.3, 249.3, 174.5, 170.1, 189.1, 152.0, 181.7, 181.7, 192.1, 178.7, 62.2, 201.6, 201.6],
    "Nov": [9.6, 15.7, 10.0, 15.6, 8.9, 16.0, 9.8, 3.8, 2.2, 70.7, 2.2, 56.7, 10.1, 97.1, 195.4, 195.4, 125.5, 160.3, 249.3, 174.5, 170.1, 189.1, 152.0, 181.7, 181.7, 192.1, 178.7, 62.2, 201.6, 201.6],
}

df_2017 = pd.DataFrame(data_2017)
df_2017["rain_kharif"] = df_2017[["May", "Jun", "Jul", "Aug", "Sep"]].mean(axis=1)
df_2017["rain_rabi"] = df_2017[["Oct", "Nov", "Jan", "Feb"]].mean(axis=1)

# Saving to CSV
csv_path = "rainfall_2017.csv"
df_2017[["District", "rain_kharif", "rain_rabi"]].to_csv(csv_path, index=False)