from html2image import Html2Image
from PIL import Image
import http.client
import json

hti = Html2Image()
conn = http.client.HTTPSConnection("api.coingecko.com")
coins = ["aave","cardano","algorand","avalanche-2","basic-attention-token","bitcoin-cash","bitcoin","binance-usd","compound-governance-token","dai","dogecoin","polkadot","elrond-erd-2","enjincoin","eos","ethereum","fantom","kyber-network-crystal","chainlink","litecoin","terra-luna","decentraland","maker","omisego","pax-gold","shiba-inu","solana","true-usd","uniswap","usd-coin","paxos-standard","tether","stellar","ripple","0x","tezos"]

def create_image(symbol, finalData, color):
    text_file = open("index.html", "r")
    data = text_file.read()
    data = data.replace("${final_data}", finalData)
    data = data.replace("${color}", color)
    text_file.close()
    hti.screenshot(html_str=data, save_as='red_page.png', size=(200, 150))
    img = Image.open("./red_page.png")
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for items in datas:
        if items[0] == 255 and items[1] == 255 and items[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(items)

    img.putdata(newData)
    img.save("./" + symbol + ".png", "PNG")


def get_ohlc_data(symbol):
    payload = ''
    headers = {
        'accept': 'application/json'
    }
    conn.request("GET", "/api/v3/coins/" + symbol + "/ohlc?vs_currency=usd&days=1", payload, headers)
    response = conn.getresponse()

    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    return json_obj


def fetch_OHLC_image(symbol):
    data = get_ohlc_data(symbol)
    finalData = ""
    color = "#4caf50" if data[0][2] < data[len(data) - 1][2] else "#f44336"
    for val in data:
        finalData = finalData + "[" + str(val[0]) + "," + str(val[2]) + "],"
    create_image(symbol, finalData, color)


for coin in coins:
    fetch_OHLC_image(coin)
