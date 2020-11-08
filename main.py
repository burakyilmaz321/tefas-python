import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI


app = FastAPI()

@app.get("/fund/{code}")
def fund_info(code: str):
    code = code.upper()
    endpoint = f"https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={code}"
    res = requests.get(endpoint)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')
    else:
        return {"msg": "Something happened", "status_code": res.status_code}
    soup = BeautifulSoup(res.content, 'html.parser')
    name = soup.find("span", id="MainContent_FormViewMainIndicators_LabelFund")
    name = name.text
    main_indicators = soup.select("#MainContent_PanelInfo > div.main-indicators > ul.top-list > li")
    main_indicators = {i.contents[0]: i.span.text for i in main_indicators}
    main_indicators = {
        "last_price": convert_last_price(main_indicators["Son Fiyat (TL)"]),
        "daily_return": convert_return(main_indicators["Günlük Getiri (%)"]),
    }
    price_indicators = soup.select("#MainContent_PanelInfo > div.price-indicators > ul > li")
    price_indicators = {i.contents[0]: i.span.text for i in price_indicators}
    price_indicators = {
        "return_1m": convert_return(price_indicators["Son 1 Ay Getirisi"]),
        "return_3m": convert_return(price_indicators["Son 3 Ay Getirisi"]),
        "return_6m": convert_return(price_indicators["Son 6 Ay Getirisi"]),
        "return_12m": convert_return(price_indicators["Son 1 Yıl Getirisi"]),
    }
    response = {
        "name": name,
        "code": code,
        **main_indicators,
        **price_indicators,
    }
    return response

def convert_last_price(s):
    return format(float(s.replace(",", ".")), ".8f")

def convert_return(s):
    return format(float(s.replace(",", ".").replace("%", "")) / 100, ".8f")
