import asyncio
from dataclasses import dataclass
from binance_data import BinanceData
from typing import Callable
import httpx

@dataclass
class MarketDepth:
    time_updated: str
    bid_level: list
    ask_level: list

async def fetch_forever(http_func: Callable[httpx.AsyncClient, asyncio.Semaphore],
                        cycle_per_second: float = 2) -> None:
    semaphore = asyncio.Semaphore(self.MAX_CONCURRENT)
    second_per_cycle = 1/cycle_per_second
    async with httpx.AsyncClient() as client:
        while (True):
            cycle_start = time.time()
            print(f'Cycle start: {cycle_start}')
            await http_func(client, semaphore)

            # use another await here to update the dashboard!
            cycle_end = time.time()
            cycle_time = cycle_end-cycle_start
            if (cycle_time < second_per_cycle):
                time.sleep(second_per_cycle-cycle_time)
    return

def main() -> None:
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT']
    md = {symbol: MarketDepth() for symbol in symbols}

    return

if __name__ == '__main__':
    main()