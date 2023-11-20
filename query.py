import bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen

def query(site):
    with urlopen(site) as response:
        soup = BeautifulSoup(response, 'html.parser')
    return parse(soup)

def parse(soup):
    for section in soup.find_all("section"):
        racename = section.h2.string
        for race in section:
            table_headers = []
            entries = []
            for child in race:
                if type(child) != bs4.element.Tag:
                    continue
                if child.name == "span" and any(["EventResults_eventMeta" in obj for obj in child["class"]]):
                    print(f"Race: {racename} {child.get_text()}")
                if child.name == "div" and any(["EventResults_tableWrap" in obj for obj in child["class"]]):
                    print(f"Result:")
                    for row in child.find_all(attrs={"role": "row"}):
                        is_header = False
                        for ic, cell in enumerate(row):
                            if cell.name == "th":
                                table_headers.append(cell.get_text())
                                is_header = True
                            elif cell.name == "td":
                                if ic == 0:
                                    entries.append([])
                                entries[-1].append(cell.get_text())
                            else:
                                fatal(f"Thats a weird cell: {cell.name}")
                        print(table_headers if is_header else entries[-1])
                        
                            
