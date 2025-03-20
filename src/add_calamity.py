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

"""
Year Normal Actual Deviation    Natural Calamities
     Rain-  Rain-  from Normal
     fall   fall   in mm  in %
2010 1451.2 1293.0 -158.2 -10.9 Flood, Heavy Rain, Drought & Unseasonal Cyclonic Rain
2011 1451.2 1338.1 -113.1 -7.8 Drought & Flood
2012 1451.2 1384.1 -67.1 -4.6 Drought & Flood
2013 1451.2 1653.1 201.9 13.9 Very Severe Cyclonic Storm "Phailin"/Flood
2014 1451.2 1608.7 157.5 10.9 Very Severe Cyclonic Storm "Hudhud"/Flood
2015 1451.2 1224.8 -226.4 -15.6 Drought, Flood & Heavy Rain
2016 1451.2 1283.1 -168.1 -11.6 Drought, Flood & Heavy Rain
2017 1451.2 1336.4 -114.8 -7.9 Flood, Heavy Rain, Drought & Pest AƩack, Unseasonal Rain
2018 1451.2 1643.3 192.1 13.2 Cyclonic Storm "Titli"
2019 1451.2 1627.8 176.6 12.2 Extremely Severe Cyclonic Storm "Fani" & “Bulbul”
"""

calamity_scores = {
    2010: 6.5, 2011: 4.5, 2012: 4.0, 2013: 9.0, 2014: 8.5,
    2015: 5.5, 2016: 5.0, 2017: 5.5, 2018: 7.5, 2019: 9.5
}

districts = [
    "ANGUL", "BALASORE", "BARGARH", "BHADRAK", "BOLANGIR", "BOUDH", "CUTTACK", "DEOGARH", "DHENKANAL", "GAJAPATI",
    "GANJAM", "JAGATSINGHPUR", "JAJPUR", "JHARSUGUDA", "KALAHANDI", "KANDHAMAL", "KENDRAPARA", "KEONJHAR", "KHORDHA", "KORAPUT",
    "MALKANGIRI", "MAYURBHANJ", "NABARANGPUR", "NAYAGARH", "NUAPADA", "PURI", "RAYAGADA", "SAMBALPUR", "SUBARNAPUR", "SUNDARGARH"
]

for district in districts:
    file_name = f"dist_{district.upper()}.csv"
    df = pd.read_csv(file_name)
    
    df["calamity_severity"] = df["Year"].map(calamity_scores)
    
    df.to_csv(file_name, index=False)

print("Calamity severity scores added successfully.")