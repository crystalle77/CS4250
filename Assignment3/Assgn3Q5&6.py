import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["cs_crawler"]
pages_collection = db["pages"]

# Initial URL and frontier
base_url = "https://www.cpp.edu/sci/computer-science/"
target_url = "https://www.cpp.edu/sci/computerscience/faculty-and-staff/permanent-faculty.shtml"

frontier = [base_url]
visited = set()

def retrieveHTML(url):
    """Retrieve the HTML content of a URL."""
    try:
        with urllib.request.urlopen(url) as response:
            if "text/html" in response.getheader("Content-Type"):
                return response.read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def parse(html):
    """Parse HTML to extract all valid links."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        full_url = urljoin(base_url, href)
        if full_url.startswith(base_url) and full_url not in visited:
            links.append(full_url)
    return links

def storePage(url, html):
    """Store the HTML data in MongoDB."""
    pages_collection.insert_one({"url": url, "html": html})

def isTargetPage(html):
    """Check if the current page is the target page."""
    soup = BeautifulSoup(html, "html.parser")
    h1_tag = soup.find("h1", class_="cpp-h1")
    return h1_tag and "Permanent Faculty" in h1_tag.text

# Main crawler procedure
while frontier:
    url = frontier.pop(0)
    if url in visited:
        continue

    visited.add(url)
    print(f"Visiting: {url}")
    html = retrieveHTML(url)
    
    if html:
        storePage(url, html)
        if isTargetPage(html):
            print(f"Target page found: {url}")
            break
        frontier.extend(parse(html))
    else:
        print(f"Skipping {url} due to retrieval failure.")
