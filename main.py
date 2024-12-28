import requests
from bs4 import BeautifulSoup
import pandas as pd

pages_to_fetch = 200

ranks = [
    "Legendary Grandmaster",
    "International Grandmaster",
    "Grandmaster",
    "International Master",
    "Master",
    "Candidate Master",
    "Expert",
    "Specialist",
    "Pupil",
    "Newbie"
]


def get_rank_bounds(rank: str) -> tuple[int, int]:
    match rank:
        case "Legendary Grandmaster":
            return (3000, 3999)
        case "International Grandmaster":
            return (2600, 2999)
        case "Grandmaster":
            return (2400, 2599)
        case "International Master":
            return (2300, 2399)
        case "Master":
            return (2100, 2299)
        case "Candidate Master":
            return (1900, 2099)
        case "Expert":
            return (1600, 1899)
        case "Specialist":
            return (1400, 1599)
        case "Pupil":
            return (1200, 1399)
        case "Newbie":
            return (0, 1199)


def get_rank_from_rating(rating: int) -> str:
    for rank in ranks:
        min_rating, max_rating = get_rank_bounds(rank)
        if min_rating <= rating <= max_rating:
            return rank
    raise NotImplementedError


data = []

for page in range(1, pages_to_fetch + 1):
    html = requests.get(f"https://codeforces.net/ratings/page/{page}").text
    soup = BeautifulSoup(html, features="html.parser")
    table = soup.find("div", {"id": "pageContent"}).find("table")
    lower_count = 0
    higher_count = 0
    for row in table.find_all("tr"):
        if row.find("td") is None:
            continue
        fields = row.find_all("td")
        position = int(fields[0].text.strip())
        handle = fields[1].text.strip()
        rating = int(fields[3].text.strip())
        rank = ' '.join(row.find("a")["title"].split()[:-1])
        actual_rank = get_rank_from_rating(rating)
        if actual_rank != rank:
            data.append([position, handle, rating, actual_rank, ranks.index(actual_rank), rank, ranks.index(rank)])
    print(f"parsed page {page}")

df = pd.DataFrame(data, columns=["position", "handle", "rating", "rank_from", "index_from", "rank_to", "index_to"])
df.to_csv("log.csv")
