import asyncio
import requests
import time
import logging
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Launchpad URL for Ubuntu mirrors
URL = "https://launchpad.net/ubuntu/+archivemirrors"
MAX_CONCURRENT_REQUESTS = 10

async def fetch_mirror(session, url):
    """Fetch a URL and return the status code and ping time."""
    start_time = time.time()
    try:
        logger.info(f"Fetching {url}...")
        async with session.get(url, timeout=10) as response:
            ping_time = time.time() - start_time
            logger.info(f"Successfully fetched {url} with status {response.status}.")
            return url, response.status, ping_time
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return url, str(e), None

async def fetch_all_mirrors(mirrors):
    """Fetch all mirrors with limited concurrency."""
    async with ClientSession() as session:
        tasks = []
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)  # Limit concurrent requests

        async def fetch_with_semaphore(url):
            async with semaphore:
                return await fetch_mirror(session, url)

        for mirror in mirrors:
            for link in mirror['links']:
                if link.startswith('http'):
                    tasks.append(fetch_with_semaphore(link))  # Use the semaphore-controlled fetch

        return await asyncio.gather(*tasks)

def get_up_to_date_mirrors():
    """Retrieve up-to-date mirrors from Launchpad."""
    logger.info("Retrieving up-to-date mirrors from Launchpad...")
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    mirrors_table = soup.select_one("div.top-portlet #mirrors_list tbody")

    mirrors = []
    current_country = ""

    for row in mirrors_table.find_all("tr"):
        if "class" in row.attrs and "head" in row.attrs["class"]:
            current_country = row.th.get_text(strip=True)
        elif "class" not in row.attrs:
            columns = row.find_all("td")
            if len(columns) >= 4:
                mirror_name = columns[0].get_text(strip=True)
                mirror_links = [a['href'] for a in columns[1].find_all('a')]
                bandwidth = columns[2].get_text(strip=True)
                status = columns[3].get_text(strip=True)

                if "Up to date" in status:
                    mirrors.append({
                        "country": current_country,
                        "name": mirror_name,
                        "links": mirror_links,
                        "bandwidth": bandwidth
                    })
    
    logger.info(f"Found {len(mirrors)} up-to-date mirrors.")
    return mirrors

def main():
    mirrors = get_up_to_date_mirrors()
    logger.info("Starting to fetch mirror statuses and ping times...")
    results = asyncio.run(fetch_all_mirrors(mirrors))

    # Collect mirrors with successful status and their ping times
    successful_mirrors = [
        (url, status, ping) for url, status, ping in results if ping is not None and status == 200
    ]

    # Sort mirrors by ping time (ascending)
    successful_mirrors.sort(key=lambda x: x[2])

    # Print top 10 successful mirrors with their status and ping
    logger.info("Top 10 Up-to-Date Ubuntu Mirrors (HTTP):")
    for url, status, ping in successful_mirrors[:10]:
        logger.info(f"URL: {url}, Status: {status}, Ping: {ping:.2f}s")

if __name__ == "__main__":
    main()
