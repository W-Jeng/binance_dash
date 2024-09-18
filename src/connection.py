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

class BinanceConnection:
    '''
    This establishes binance connection using multiple websocket
    '''
    BASE_URL = 'https://api.binance.com/api/v3/depth'
    MARKET_DEPTH = 5
    MAX_CONCURRENT = 5  

    def __init__(self, symbols):
        self.symbols = symbols

    async def fetch_one(self, client: httpx.AsyncClient,
                        semaphore: asyncio.Semaphore,
                        symbol: str) -> None:
        # establish single connection
        print(f'Initiating connection on symbol: {symbol}')
        params = {
            'symbol': symbol,
            'limit': self.MARKET_DEPTH 
        }
        async with semaphore:
            response = await client.get(self.BASE_URL, params=params)    
            response.raise_for_status()

        return ResponseObject(symbol=symbol, data=response.json())

    async def fetch_multiple(self) -> None:
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT)
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch_one(client, semaphore, symbol) for symbol in self.symbols]
            for coroutine_obj in asyncio.as_completed(tasks):
                resp = await coroutine_obj
                print(resp)
        return

if __name__ == '__main__':
    start_time = time.time()
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'SOLUSDT']
    binance_connection = BinanceConnection(symbols)
    asyncio.run(binance_connection.fetch_multiple())
    end_time = time.time()
    print(f'Time taken: {round(end_time-start_time,4)}')


