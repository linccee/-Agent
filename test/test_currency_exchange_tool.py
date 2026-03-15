
from tools.currency_exchange_tool import currency_exchange

if __name__ == "__main__":
    query = '{"base_code": "CNY", "target_code": "USD", "amount": "100"}'
    print(currency_exchange.invoke(query))