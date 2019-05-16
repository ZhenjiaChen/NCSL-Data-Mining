from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

# Load fips codes
json_file_path = "../fips codes/fips_codes_all.json"
with open(json_file_path) as f:
    fips_dict = json.load(f)

# Load page
page_url = "http://www.ncsl.org/research/redistricting/redistricting-criteria.aspx"
response = requests.get(page_url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", attrs={"class":"footable table toggle-circle table-hover table-condensed table-bordered"})
table_body = table.find("tbody")

# Parse data
data = []
rows = table_body.find_all("tr")
for row in rows:
    cols = row.find_all("td")
    cols = [cell.text.strip() for cell in cols]
    data.append(cols)

row_index_tuples = [(data[2*int(c/2)][0],data[c][1]) for c in range(len(data))]
data_array = []
keywords = ["compact",
            "contiguous",
            "political subdivisions",
            "communities of interest",
            "preserve cores",
            "avoid pairing",
            "favor or disfavor",
            "partisan data",
            "competitive",
            "partisan advantage"]

# Formating data_array
for i in range(len(data)):
    entry = data[i]
    state = data[2*int(i/2)][0]
    criteria = entry[2]
    criteria = criteria.lower()

    allowed_idx = criteria.find("allowed") if criteria.find("allowed") != -1 else len(criteria)+1
    prohibited_idx = criteria.find("prohibited") if criteria.find("prohibited") != -1 else len(criteria)+1

    entry_array = [fips_dict[state]["numeric"]]
    for word in keywords:
        if word in criteria[0:allowed_idx] and word in criteria[0:prohibited_idx]:
            entry_array.append("R")
        elif word in criteria[allowed_idx:prohibited_idx]:
            entry_array.append("A")
        elif word in criteria[prohibited_idx:]:
            entry_array.append("P")
        else:
            entry_array.append("")
    data_array.append(entry_array)

# Make dataframe
row_index = pd.MultiIndex.from_tuples(row_index_tuples, names=['State','Legislative or Congressional'])
df = pd.DataFrame(data_array,
                  index = row_index,
                  columns = ["FIPS Code",
                             "Compactness",
                             "Contiguity of Districts",
                             "Preservation of Political Subdivisions",
                             "Preservation of Communities of Interest",
                             "Preservation of cores of prior districts",
                             "Avoid pairing incumbents",
                             "Favor or disfavor and incumbent or candidate",
                             "Using partisan data",
                             "Competitiveness",
                             "Preserving partisan advantage"])

if __name__ == "__main__":
    print(fips_dict)

    with open("redistrcting_all.csv", mode='w') as f:
        df.to_csv(f)
