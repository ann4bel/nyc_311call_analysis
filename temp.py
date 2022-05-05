import pandas as pd
from sodapy import Socrata
import numpy as np
import statsmodels.formula.api as smf

# import 311 data from Socrata

client = Socrata("data.cityofnewyork.us", None)
# returned as JSON from API / converted to Python list of dictionaries by sodapy.
data_id_2008 = "uzcy-9puk"
data_id_2007 = "aiww-p3af"
data_2008 = client.get(data_id_2008)
data_2007 = client.get(data_id_2007)
# Convert to pandas DataFrame
df08 = pd.DataFrame.from_records(data_2008)
df07 = pd.DataFrame.from_records(data_2007)

# take a random sample (n = 3,000) from df2008 and df2007
df08 = df08.sample(n=6000, replace=True)
df07 = df07.sample(n=6000, replace=True)

# "created_date" column
# separate each call from the dataset by day and convert into dataframe
d = dict()
avgtemp07 = {1: 37.5, 2: 28.2, 3: 42.2, 4: 50.3, 5: 65.2, 6: 71.4, 7: 75, 8: 74, 9: 70.3, 10: 63.6, 11: 45.4, 12: 37}
avgtemp08 = {1: 36.5, 2: 35.8, 3: 42.6, 4: 54.9, 5: 60.1, 6: 74, 7: 78.4, 8: 73.8, 9: 68.8, 10: 55.1, 11: 45.8, 12: 38.1}
for index, row in df08.iterrows():
    date = row["created_date"][:10]
    if date not in d:
        d[date] = [0]*3
        month = int(date[5:7])
        d[date][0] += 1
        d[date][1] = avgtemp08[month]
        d[date][2] = 1
    else:
        d[date][0] += 1
for index, row in df07.iterrows():
    date = row["created_date"][:10]
    if date not in d:
        d[date] = [0] * 3
        month = int(date[5:7])
        d[date][0] += 1
        d[date][1] = avgtemp07[month]
        d[date][2] = 0
    else:
        d[date][0] += 1
df = pd.DataFrame.from_dict(d, orient='index', columns=["count311", "avgtemp", "y2008"])
m = smf.ols(formula="count311 ~ y2008 + avgtemp", data=df).fit()
print(m.summary())