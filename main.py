import ccxt
import time

exchange = ccxt.bybit({"enableRateLimit": True})
exchange.load_markets()

triangles = [
    ("BTC/USDT", "ETH/USDT", "ETH/BTC"),
    ("BTC/USDT", "SOL/USDT", "SOL/BTC"),
    ("BTC/USDT", "XRP/USDT", "XRP/BTC"),
    ("BTC/USDT", "DOGE/USDT", "DOGE/BTC"),
]
start_usdt = 100.0
fee = 0.001

while True:
    try:
        for pair1, pair2, pair3 in triangles:
            if not all(p in exchange.markets for p in (pair1, pair2, pair3)):
                print(f"Пропуск {pair1}+{pair2}+{pair3}: пары нет на бирже")
                print("-" * 40)
                continue
            tickers = exchange.fetch_tickers([pair1, pair2, pair3])

            ask_pair1 = tickers[pair1]["ask"]
            bid_pair2 = tickers[pair2]["bid"]
            ask_pair3 = tickers[pair3]["ask"]

            btc_bought = (start_usdt / ask_pair1) * (1 - fee)
            eth_bought = (btc_bought / ask_pair3) * (1 - fee)
            final_usdt = (eth_bought * bid_pair2) * (1 - fee)
            profit = final_usdt - start_usdt
            profit_pct = (final_usdt / start_usdt - 1) * 100

            implied = bid_pair2 / ask_pair1
            diff = (tickers[pair3]["bid"] / implied)

            print(f"{pair1} + {pair2} + {pair3}")
            print(f"  {pair1} ask: {ask_pair1}")
            print(f"  {pair2} bid: {bid_pair2}")
            print(f"  {pair3} ask: {ask_pair3}")
            print(f"  Старт: {start_usdt} USDT -> Финиш: {final_usdt:.4f} USDT")
            print(f"  Профит: {profit:.4f} USDT ({profit_pct:.4f}%)")

            if profit > 0:
                print("  >>> Цикл прибыльный!")
            else:
                print("  Цикл убыточный (комиссии съедают)")

            print("-" * 40)

        time.sleep(5)

    except Exception as e:
        print("Ошибка:", e)
        time.sleep(5)