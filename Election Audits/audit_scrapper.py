from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

# Load fips codes
json_file_path = "../fips codes/fips_codes_all.json"
with open(json_file_path) as f:
    fips_dict = json.load(f)

# Load page
page_url = "http://www.ncsl.org/research/elections-and-campaigns/post-election-audits635926066.aspx"
response = requests.get(page_url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table")
table_body = table.find("tbody")

# Pasrse data
data = []
rows = table_body.find_all("tr")[1:] # ignore first row
for row in rows:
    cols = row.find_all("td")
    cols = [cell.text.strip() for cell in cols]
    data.append(cols)

# Formating data_array
data_array = []
row_index = []
for i in range(len(data)):
    entry = data[i]

    possible_states = []
    for s in fips_dict:
        if s in entry[0]:
            possible_states.append(s)
    state = max(possible_states, key=lambda x:len(x))
    row_index.append(state)
    data_array.append([fips_dict[state]["numeric"],
                       entry[1]])

# Make dataframe
df = pd.DataFrame(data_array,
                  index = row_index,
                  columns = ["FIPS Code",
                             "Audit Type"])

if __name__ == "__main__":
    with open("audit.csv", mode='w') as f:
        df.to_csv(f)
