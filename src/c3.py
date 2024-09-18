import httpx
import asyncio

# Define a semaphore with a max of 5 concurrent requests
semaphore = asyncio.Semaphore(5)

async def fetch(url: str, client: httpx.AsyncClient) -> str:
    # Use the semaphore to limit concurrent requests
    async with semaphore:
        response = await client.get(url)
        return response.text

async def main():
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    urls = [url for _ in range(20)]  # List of URLs to fetch (for demonstration)

    async with httpx.AsyncClient() as client:
        # Schedule fetch tasks with a semaphore
        tasks = [fetch(url, client) for url in urls]
        results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

# Run the main function
asyncio.run(main())
