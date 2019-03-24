from bs4 import BeautifulSoup
import requests
import json

page_url = "https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code"
response = requests.get(page_url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", attrs={"class":"wikitable sortable"})
table_body = table.find("tbody")

data = []
rows = table_body.find_all("tr")
for row in rows:
    cols = row.find_all("td")
    cols = [cell.text.strip() for cell in cols]
    data.append(cols)

codes_dict = {}

for row in data[1:]:
    name = row[0]
    alpha_code = row[1]
    numeric_code = row[2]
    codes_dict[name] = {"alpha":alpha_code,
                        "numeric":numeric_code}
# print(str(codes_dict))
with open("fips_codes.json", "w") as f:
    json.dump(codes_dict, f)
