from fastapi import FastAPI
import requests

app = FastAPI(title="Currency Rates")
API_KEY = "1b033a7d529b9cfc8223511a"


def fetch_rates(currency: str):
    base_url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency.upper()}"
    response = requests.get(base_url)

    if response.status_code != 200:
        error_message = f"Failed to fetch data, status code: {response.status_code}, response text: {response.text}"
        print(error_message)
        return None, error_message

    all_rates = response.json().get("conversion_rates", {})
    selected_currencies = ["USD", "KZT", "RUB", "EUR", "KGS", "JPY", "UZS"]
    rates = {cur: all_rates[cur] for cur in selected_currencies if cur in all_rates}

    return rates, None


@app.get("/currency_rates/", tags=['currencies'])
def get_rates(currency: str = "KGS"):
    rates, error = fetch_rates(currency)
    if error:
        return {"error": error}

    return {"base_currency": currency.upper(), "rates": rates}


@app.get("/convert/{amount}", tags=['currencies'])
def convert_currency(currency: str = "KGS", amount: float = 1):
    rates, error = fetch_rates(currency)
    if error:
        return {"error": error}

    converted_amounts = {cur: rate * amount for cur, rate in rates.items()}
    return {"base_currency": currency.upper(), "amount": amount, "converted_amounts": converted_amounts}
