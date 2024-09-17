import requests

class BinanceDepth:
    '''
    This class fetches market depth data from Binance using HTTP requests.
    '''
    BASE_URL = 'https://api.binance.com/api/v3/depth'

    def __init__(self, symbols, limit=5):
        self.symbols = symbols
        self.limit = limit

    def fetch_depth(self, symbol: str):
        # Ensure the symbol is in uppercase
        symbol = symbol.upper()
        params = {
            'symbol': symbol,
            'limit': self.limit  # Number of order book levels to retrieve
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            print(f'symbol: {symbol}, DATA: {data}')
        except requests.exceptions.RequestException as e:
            print(f'Error fetching data for {symbol}: {e}')

    def fetch_all_depths(self):
        for symbol in self.symbols:
            self.fetch_depth(symbol)

if __name__ == '__main__':
    symbols = ['BTCUSDT', 'ETHUSDT']
    binance_depth = BinanceDepth(symbols, limit=5)  # Adjust the limit as needed
    binance_depth.fetch_all_depths()
