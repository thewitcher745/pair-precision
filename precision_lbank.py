import json
import requests

# Import the list of coins from the logo_list.json file
with open("./logo_list.json", "r", encoding="utf-8") as f:
    coin_list = list(json.load(f).keys())

precisions = {}
count = len(coin_list)
for i, coin in enumerate(coin_list):
    data_points = requests.get(
        f"https://api.lbank.info/v2/ticker/24hr.do?symbol={coin.lower()}_usdt"
    )

    if data_points.status_code != 200:
        continue

    json_result = data_points.json()
    if "data" not in json_result or len(json_result["data"]) == 0:
        continue

    price_samples = [
        json_result["data"][0]["ticker"]["low"],
        json_result["data"][0]["ticker"]["high"],
        json_result["data"][0]["ticker"]["latest"],
    ]
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
with open("./precisions_lbank.csv", "w") as f:
    for coin, precision in precisions.items():
        f.write(f"{coin},{precision}\n")
