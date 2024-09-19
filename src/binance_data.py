import asyncio
import websockets
import json
import httpx
import time
from dataclasses import dataclass

@dataclass
class ResponseObject:
    symbol: str
    data: dict

class BinanceData:
    '''
    This establishes binance connection using multiple websocket
    '''
    BASE_URL = 'https://api.binance.com/api/v3/depth'
    MARKET_DEPTH = 5
    MAX_CONCURRENT = 10  

    def __init__(self, symbols):
        self.symbols = symbols

    async def fetch_one(self, client: httpx.AsyncClient,
                        semaphore: asyncio.Semaphore,
                        symbol: str) -> None:
        # establish single connection
        params = {
            'symbol': symbol,
            'limit': self.MARKET_DEPTH 
        }
        async with semaphore:
            response = await client.get(self.BASE_URL, params=params)    
            response.raise_for_status()

        return ResponseObject(symbol=symbol, data=response.json())

    async def fetch_multiple(self, client: httpx.AsyncClient, semaphore: asyncio.Semaphore) -> None:
        tasks = [self.fetch_one(client, semaphore, symbol) for symbol in self.symbols]
        for coroutine_obj in asyncio.as_completed(tasks):
            resp = await coroutine_obj
            print(resp)
        return

    async def fetch_forever(self, cycle_per_second: float = 2) -> None:
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT)
        second_per_cycle = 1/cycle_per_second
        async with httpx.AsyncClient() as client:
            while (True):
                cycle_start = time.time()
                print(f'Cycle start: {cycle_start}')
                await self.fetch_multiple(client, semaphore)
                cycle_end = time.time()
                cycle_time = cycle_end-cycle_start
                if (cycle_time < second_per_cycle):
                    time.sleep(second_per_cycle-cycle_time)
        return

if __name__ == '__main__':
    start_time = time.time()
    binance_data = BinanceData(symbols)
    asyncio.run(binance_data.fetch_forever(0.5))
    end_time = time.time()
    print(f'Time taken: {round(end_time-start_time,4)}')


