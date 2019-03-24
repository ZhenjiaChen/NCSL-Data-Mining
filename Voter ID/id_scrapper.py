from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

# Load FIPS codes
json_file_path = "../fips codes/fips_codes_states.json"
with open(json_file_path) as f:
    fips_dict = json.load(f)

# Load page
page_url = "http://www.ncsl.org/research/elections-and-campaigns/voter-id.aspx"
response = requests.get(page_url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", attrs={"class":"table table-bordered table-condensed table-hover"})
table_body = table.find("tbody")

# Parse data
data = []
rows = table_body.find_all("tr")
for row in rows:
    cols = row.find_all("td")
    cols = [cell.text.strip() for cell in cols]
    data.append(cols)

# Formating data_array
data_dict = {}

whitelist = list(map(chr,[x for x in range(65,123) if x not in range(91,97)]))+[" ","\n"]
def mark_states(input, attr, label):
    input_split = ''.join(filter(lambda x: x in whitelist, input)).split("\n")
    input_split = [x.strip() for x in input_split]
    for state in input_split:
        data_dict[state] = {attr: label}

mark_states(data[1][1], "Photo ID", "S")
mark_states(data[1][2], "Non-Photo ID", "S")
mark_states(data[2][1], "Photo ID", "N")
mark_states(data[2][2], "Non-Photo ID", "N")

data_array = [[code["numeric"],
              data_dict.get(state,{}).get("Photo ID",""),
              data_dict.get(state,{}).get("Non-Photo ID","")] for state,code in fips_dict.items()]

df = pd.DataFrame(data_array,
                  index = fips_dict.keys(),
                  columns = ["FIPS Code","Photo ID","Non-Photo ID"])

if __name__ == "__main__":
    print(df)
    with open("voter_id.csv", mode='w') as f:
        df.to_csv(f)
