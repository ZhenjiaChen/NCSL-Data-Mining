from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import ast

# Load fips codes
json_file_path = "../fips codes/fips_codes_all.json"
with open(json_file_path) as f:
    fips_dict = json.load(f)
    fips_dict["D.C."] = {"alpha": "DC", "numeric": "11"}

# Load page
page_url = "http://www.ncsl.org/research/elections-and-campaigns/absentee-and-early-voting.aspx"
response = requests.get(page_url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find_all("table")[1]
table_body = table.find("tbody")

# Parse data
data = []
rows = table_body.find_all("tr")
for row in rows:
    cols = row.find_all("td")
    cols = [cell.text.strip() for cell in cols]
    data.append(cols)

# Format data array
data_array = str([[fips_dict.get(row[0],{}).get("numeric","N/A")]+row[1:] for row in data[1:]])
replace_dict = {"\'\'": "0",
                u"\u25cf": "1",
                "(a)": "2",
                "(b)": "3",
                "(c)": "4"}
for i,j in replace_dict.items():
    data_array = data_array.replace(i,j)
row_idx = [row[0] for row in data[1:]]          # row index by states

# print(str(data).replace(u"\u25cf","*"))
df = pd.DataFrame(ast.literal_eval(data_array),
                     index = row_idx,
                     columns = ["FIPS Code"]+data[0][1:])

if __name__ == "__main__":
    # print(df)
    df.to_csv("absentee.csv")
    # for row in ast.literal_eval(data_array):
    #     if row[0] == fips_dict.get("South Carolina").get("numeric"):
    #         print(row)
