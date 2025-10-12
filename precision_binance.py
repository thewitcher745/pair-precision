import json
import requests

# Import the list of coins from the logo_list.json file
with open("./logo_list.json", "r", encoding="utf-8") as f:
    coin_list = list(json.load(f).keys())

precisions = {}
count = len(coin_list)
for i, coin in enumerate(coin_list):
    data_points = requests.get(
        f"https://fapi.binance.com/fapi/v1/klines?symbol={coin}USDT&interval=1d&limit=2"
    )

    if data_points.status_code != 200:
        continue

    price_samples = []
    for data_point in data_points.json():
        price_samples.extend(data_point[1:5])
    precision = max([len(str(price).split(".")[1]) for price in price_samples])
    precisions[coin] = precision
    print(f"{i}/{count} {coin} {precision}")

# Write the precisions to a CSV file, with the first column being the coin name and the second column being the precision
with open("./precisions_binance.csv", "w") as f:
    for coin, precision in precisions.items():
        f.write(f"{coin},{precision}\n")
