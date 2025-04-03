import aiohttp
import pandas as pd

from io import BytesIO
from bs4 import BeautifulSoup

async def get_usd_uah_rate() -> float | None:
    url = "https://privatbank.ua/rates-archive"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Error while loading page: {response.status}")
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            pair_divs = soup.find_all("div", class_="currency-pairs")
            for div in pair_divs:
                names_div = div.find("div", class_="names")
                if names_div:
                    names_text = names_div.get_text(strip=True)

                    if "USD" in names_text and "UAH" in names_text:
                        purchase_div = div.find("div", class_="purchase")
                        sale_div = div.find("div", class_="sale")
                        if purchase_div and sale_div:
                            purchase_rate = float(purchase_div.find("span").get_text(strip=True))
                            return purchase_rate
            return None


def create_excel_file(data: list) -> BytesIO:

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Expenses")
    output.seek(0)

    return output