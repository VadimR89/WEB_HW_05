import argparse
import asyncio
from datetime import datetime, timedelta
import aiohttp


async def fetch_exchange_rate(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?date={date}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return None


async def get_exchange_rates(currency_codes, days):
    base_date = datetime.now().date()

    for i in range(1, days + 1):
        current_date = base_date - timedelta(days=i)
        formatted_date = current_date.strftime("%d.%m.%Y")

        data = await fetch_exchange_rate(formatted_date)
        if data:
            rates = data.get('exchangeRate')
            for code in currency_codes:
                rate = next((r['purchaseRateNB'] for r in rates if r['currency'] == code), None)
                if rate:
                    print(f"Date: {formatted_date}, {code} Rate: {rate}")
                else:
                    print(f"No data available for {code} on {formatted_date}")
        else:
            print(f"Failed to fetch data for {formatted_date}")


def main():
    parser = argparse.ArgumentParser(description='Retrieve exchange rates from PrivatBank API')
    parser.add_argument('currency', nargs='+', help='Currency code(s) to retrieve rates for (e.g., USD EUR)')
    parser.add_argument('--days', type=int, default=10, help='Number of days to retrieve rates for (default: 10)')

    args = parser.parse_args()

    asyncio.run(get_exchange_rates(args.currency, args.days))


if __name__ == "__main__":
    main()

"""run from console: python main.py USD EUR GBP --days 5"""
