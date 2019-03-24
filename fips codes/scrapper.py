from bs4 import BeautifulSoup
import sys
import requests
import json

def get_all_fips():
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
    return codes_dict

def get_state_fips():
    page_url = "https://www.census.gov/geo/reference/ansi_statetables.html"
    response = requests.get(page_url, timeout=5)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", attrs={"summary":"table showing ANSI state codes for the states and the District of Columbia"})
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
        alpha_code = row[2]
        numeric_code = row[1]
        codes_dict[name] = {"alpha":alpha_code,
                            "numeric":numeric_code}
    return codes_dict

if __name__ == "__main__":
    if sys.argv[0] == "all":
        with open("fips_codes_all.json", "w") as f:
            json.dump(get_all_fips(), f)
    elif sys.argv[1] == "states":
        with open("fips_codes_states.json", "w") as f:
            json.dump(get_state_fips(), f)
