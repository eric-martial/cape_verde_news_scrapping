import asyncio
import random

from fake_useragent import UserAgent
from httpx import AsyncClient, HTTPTransport, HTTPStatusError, RequestError

from .scraper_logger import ScraperLogger

SENTINEL = "STOP"


class BaseScraper:
    def __init__(self, base_url, start_urls, storage_queue, database_path):
        self.base_url = base_url
        self.start_urls = start_urls
        self.storage_queue = storage_queue
        self.database_path = database_path
        self.user_agent = UserAgent()
        self.user_agents = [
            self.user_agent.chrome,
            self.user_agent.firefox,
            self.user_agent.edge,
        ]
        self.proxies = {
            "http://": HTTPTransport(proxy="http://18.230.20.205:3128"),
            "http://": HTTPTransport(proxy="http://139.59.1.14:8080"),
            "http://": HTTPTransport(proxy="http://8.219.43.134:8118"),
            "http://": HTTPTransport(proxy="http://162.223.94.164:80"),
            "http://": HTTPTransport(proxy="http://54.38.181.125:80"),
            "http://": HTTPTransport(proxy="http://162.223.94.163:80"),
            "http://": HTTPTransport(proxy="http://193.15.14.198:80"),
            "http://": HTTPTransport(proxy="http://8.219.169.172:3132"),
            "http://": HTTPTransport(proxy="http://139.162.78.109:3128"),
            "http://": HTTPTransport(proxy="http://20.210.113.32:80"),
            "http://": HTTPTransport(proxy="http://20.24.43.214:80"),
            "http://": HTTPTransport(proxy="http://20.206.106.192:80"),
            "http://": HTTPTransport(proxy="http://47.56.110.204:8989"),
            "http://": HTTPTransport(proxy="http://162.248.225.130:80"),
            "http://": HTTPTransport(proxy="http://162.248.225.11:80"),
            "http://": HTTPTransport(proxy="http://198.199.86.11:3128"),
            "http://": HTTPTransport(proxy="http://52.117.157.155:8002"),
            "http://": HTTPTransport(proxy="http://162.223.116.54:80"),
            "http://": HTTPTransport(proxy="http://162.248.225.198:80"),
            "http://": HTTPTransport(proxy="http://103.83.179.180:3125"),
            "http://": HTTPTransport(proxy="http://114.231.46.31:8089"),
            "http://": HTTPTransport(proxy="http://202.12.80.6:82"),
            "http://": HTTPTransport(proxy="http://202.12.80.8:82"),
            "http://": HTTPTransport(proxy="http://119.2.52.152:8282"),
            "http://": HTTPTransport(proxy="http://45.174.248.19:999"),
            "http://": HTTPTransport(proxy="http://79.110.197.144:8081"),
            "http://": HTTPTransport(proxy="http://183.230.162.122:9091"),
            "http://": HTTPTransport(proxy="http://181.209.111.146:999"),
            "http://": HTTPTransport(proxy="http://114.103.88.224:8089"),
            "http://": HTTPTransport(proxy="http://185.194.11.180:8080"),
            "http://": HTTPTransport(proxy="http://111.72.198.123:8089"),
            "http://": HTTPTransport(proxy="http://103.158.220.2:83"),
            "http://": HTTPTransport(proxy="http://103.31.232.174:8080"),
            "http://": HTTPTransport(proxy="http://186.125.218.147:999"),
            "http://": HTTPTransport(proxy="http://114.231.46.237:8089"),
            "http://": HTTPTransport(proxy="http://154.64.215.132:999"),
            "http://": HTTPTransport(proxy="http://213.207.195.181:8080"),
            "http://": HTTPTransport(proxy="http://154.73.29.201:8080"),
            "http://": HTTPTransport(proxy="http://154.73.28.193:8080"),
            "http://": HTTPTransport(proxy="http://95.142.223.24:56379"),
            "http://": HTTPTransport(proxy="http://193.239.58.92:8081"),
            "http://": HTTPTransport(proxy="http://102.214.106.86:1975"),
            "http://": HTTPTransport(proxy="http://115.42.45.1:80"),
            "http://": HTTPTransport(proxy="http://77.119.250.129:8080"),
        }

    async def fetch_page(self, client, page_url, max_retries=5):
        retries = 0

        while retries < max_retries:
            headers = {"User-Agent": random.choice(self.user_agents)}

            try:
                resp = await client.get(page_url, headers=headers, timeout=180)
                resp.raise_for_status()
                return resp
            except HTTPStatusError as e:
                if e.response.status_code == 502:
                    retries += 1
                    ScraperLogger.log_warning(
                        f"{page_url} \n 502 Bad Gateway. Retrying... ({retries}/{max_retries})"
                    )
                    await asyncio.sleep(2**retries)  # Exponential backoff
                else:
                    raise
            except RequestError as e:
                retries += 1
                ScraperLogger.log_warning(
                    f"{page_url} \n  Request failed. Retrying... ({retries}/{max_retries})"
                )
                await asyncio.sleep(2**retries)  # Exponential backoff

        ScraperLogger.log_error(
            f"Failed to fetch page {page_url} after {max_retries} retries."
        )

    async def send_post_request(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"

        async with AsyncClient() as client:
            try:
                response = await client.post(url, data=data)

                # Check if the request was successful (status code 2xx)
                if response.status_code // 100 == 2:
                    ScraperLogger.log_info(f"POST request to {url} successful!")
                    return response  # Return the response data
                else:
                    ScraperLogger.log_warning(
                        f"POST request to {url} failed with status code {response.status_code}. Response: {response.text}"
                    )
                    return None
            except RequestError as e:
                ScraperLogger.log_error(
                    f"An error occurred during the POST request to {url}: {e}"
                )
                return None

    async def parse_page(self, client, page_url):
        raise NotImplementedError("Subclasses must implement the parse_page method.")

    async def parse_article(self, page_url, html):
        raise NotImplementedError("Subclasses must implement the parse_article method.")

    async def run(self):
        async with AsyncClient() as client:
            for start_url in self.start_urls:
                full_url = f"{self.base_url}{start_url}"
                await self.parse_page(client, full_url)

        # Signal the storage saver to exit
        await self.storage_queue.put(SENTINEL)
