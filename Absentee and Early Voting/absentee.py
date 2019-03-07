from bs4 import BeautifulSoup
import requests
import pandas as pd
import ast

page_url = "http://www.ncsl.org/research/elections-and-campaigns/absentee-and-early-voting.aspx"
response = requests.get(page_url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", attrs={"class":"table table=bordered table-hover table-condensed"})
table_body = table.find("tbody")

data = []
rows = table_body.find_all("tr")
for row in rows:
    cols = row.find_all("td")
    cols = [cell.text.strip() for cell in cols]
    data.append(cols)

data_array = [row[1:] for row in data]
row_idx = [row[0] for row in data]

# print(str(data).replace(u"\u25cf","*"))
frame = pd.DataFrame(ast.literal_eval(str(data[1:]).replace(u"\u25cf","1").replace("\'\'","0")),
                     columns = data[0])

if __name__ == "__main__":
    print(frame)
