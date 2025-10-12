import requests, os, json
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

OLX_BASE_URL="https://www.olx.ua"
SEEN_FILE="data/seen.json"
MAX_SEEN=500


def sendNotification (message):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage"
    res = requests.post(url, {"chat_id": os.getenv("CHAT_ID"), "text": message})
    return res


seen = json.load(open(SEEN_FILE))


priceTo=9000
page=1
url = f"https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/?search%5Bdist%5D=2&search%5Border%5D=created_at:desc&search%5Bfilter_float_price:to%5D={priceTo}&currency=UAH&page={page}"


page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

listing = soup.find("div", attrs={"data-testid": "listing-grid"})
items = listing.find_all("div", attrs={"data-testid": "l-card"})


print(len(items))

for item in reversed(items): 
    # Check if already seen
    item_id = item.get("id")
    
    if item_id in seen or not item_id:
        continue
    
    # Send a notification with a link
    a_tag = item.find("a", href=True)

    if a_tag:
        link = OLX_BASE_URL + a_tag.get("href")
        sendNotification(link)

    seen.append(item_id)


json.dump(seen, open(SEEN_FILE, "w"))
