# Tefas API

Simple API for Tefas funds

## Usage

```
curl 'http://tefas.herokuapp.com/fund/YAC | jq'
```

Response

```
{
  "name": "YAPI KREDİ PORTFÖY İKİNCİ FON SEPETİ FONU",
  "code": "YAC",
  "last_price": "1.86744100",
  "daily_return": "0.00839800",
  "return_1m": "0.06158224",
  "return_3m": "0.12336062",
  "return_6m": "0.21448913",
  "return_12m": "0.36765080"
}
```

Built with Python, FastAPI and Heroku.
