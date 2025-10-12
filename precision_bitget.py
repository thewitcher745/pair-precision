import json
import requests

# Import the list of coins from the logo_list.json file
with open("./logo_list.json", "r", encoding="utf-8") as f:
    coin_list = list(json.load(f).keys())

precisions = {}
count = len(coin_list)
for i, coin in enumerate(coin_list):
    data_points = requests.get(
        f"https://api.bitget.com/api/v2/mix/market/candles?symbol={coin}USDT&granularity=5m&limit=2&productType=usdt-futures"
    )

    if data_points.status_code != 200:
        continue

    result = data_points.json()
    if result["data"] is None:
        continue

    price_samples = []
    for data_point in result["data"]:
        price_samples.extend(data_point[1:5])
    price_samples_decimal_parts = [
        str(price).split(".")[1] if "." in str(price) else "" for price in price_samples
    ]
    try:
        precision = max(
            [len(decimal_part) for decimal_part in price_samples_decimal_parts]
        )
    except Exception as e:
        print(coin, e)
        continue

    precisions[coin] = precision
    print(f"{i}/{count} {coin} {precision}")

# Write the precisions to a CSV file, with the first column being the coin name and the second column being the precision
with open("./precisions_mexc.csv", "w") as f:
    for coin, precision in precisions.items():
        f.write(f"{coin},{precision}\n")
