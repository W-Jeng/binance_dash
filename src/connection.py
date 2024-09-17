import asyncio
import websockets
import json

class BinanceConnection:
    '''
    This establishes binance connection using multiple websocket
    '''
    BASE_URL = 'https://api.binance.com/api/v3/depth'

    def __init__(self, symbols):
        self.symbols = symbols

    async def connect_s(self, symbol: str) -> None:
        # establish single connection
        print(f'Initiating connection on symbol: {symbol}')
        ws_url = f'{self.BASE_URL}{symbol}@{self.CONNECTION_INFO}'

        async with websockets.connect(ws_url) as ws:
            print(f'Connection established on url: {ws_url}')
            while (True):
                try:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    print(f'symbol: {symbol}, DATA: {data}')
                except Exception as err:
                    print(f'Error occured on symbol {symbol}; msg: {err}')
        return

    async def connect_mult(self) -> None:
        ws_coroutine = [self.connect_s(sym) for sym in self.symbols]
        await asyncio.gather(*ws_coroutine)
        return

if __name__ == '__main__':
    symbols = ['BTCUSDT']
    binance_connection = BinanceConnection(symbols)
    asyncio.run(binance_connection.connect_mult())


