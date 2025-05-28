import rnet
import asyncio
from selectolax.parser import HTMLParser
import pandas as pd


class NotAvailableElementError(Exception):
    """Custom exception for errors in the scraping process."""

    pass


def create_client() -> rnet.Client:
    return rnet.Client(
        impersonate=rnet.Impersonate.Chrome136,
        cookie_store=True,
    )


async def fetch_data(
    client: rnet.Client, urls: list[str], form_data: list[list[tuple[str, str]]] | None = None
) -> list[rnet.Response]:
    if form_data is None:
        tasks = [client.get(url) for url in urls]
        return await asyncio.gather(*tasks)
    else:
        print("Fetching data with form data...")
        tasks = [client.post(urls[0], form=form) for form in form_data]
        return await asyncio.gather(*tasks)


def parse_cities(response: str) -> list[str]:
    parser = HTMLParser(response)
    cities = parser.css(
        "#houses > div.Border_2 > div > div > form > div > table > tbody > tr > td > div.InnerTableContainer > table > tbody > tr:nth-child(2) > td > div > table > tbody > tr:nth-child(2) > td:nth-child(1) > label"
    )
    if not cities:
        raise NotAvailableElementError
    return [city.text() for city in cities]


def parse_servers(response: str) -> list[str]:
    parser = HTMLParser(response)
    servers = parser.css(
        "#houses > div.Border_2 > div > div > form > div > table > tbody > tr > td > div.InnerTableContainer > table > tbody > tr:nth-child(1) > td > div > table > tbody > tr > td > div > div.WorldSelectionDropDown > select > option"
    )
    if not servers:
        raise NotAvailableElementError
    return [server.text() for server in servers][1:]


def parse_houses(response: str) -> list[dict]:
    parser = HTMLParser(response)
    where = parser.css_first("#houses > div.Border_2 > div > div > div > div > div > div")
    if where is None:
        raise NotAvailableElementError("No house data found.")
    where = where.text()
    server = where.split(" ")[-1]
    city = where.split(" ")[-3]
    houses = parser.css(
        "#houses > div.Border_2 > div > div > div > table > tbody > tr > td > div.InnerTableContainer > table > tbody > tr > td > div > table tbody > tr"
    )[1:]
    if not houses:
        raise NotAvailableElementError
    house_data = []
    for house in houses:
        if not house.css_first("td:nth-child(2)"):
            continue
        details = {
            "name": house.css_first("td:nth-child(1)").text().replace("\xa0", " "),
            "size": house.css_first("td:nth-child(2)").text().replace("\xa0", " "),
            "rent": house.css_first("td:nth-child(3)").text().replace("\xa0", " "),
            "status": house.css_first("td:nth-child(4)").text().replace("\xa0", " "),
            "city": city,
            "server": server,
        }
        house_data.append(details)
    return house_data


def save_houses_to_file(houses: list[dict], filename: str = "houses.csv"):
    pd.DataFrame(houses).to_csv(filename, index=False)


async def main():
    client = create_client()
    url_cities = ["https://www.tibia.com/community/?subtopic=houses"]
    fetched_data = await fetch_data(client, url_cities)
    cities, servers = None, None
    for response in fetched_data:
        if response.status == 200:
            data = await response.text()
            cities = parse_cities(data)
            servers = parse_servers(data)
        else:
            raise NotAvailableElementError(f"Failed to fetch data, status code: {response.status}")
    if not cities or not servers:
        raise NotAvailableElementError("No cities or servers found.")
    form_data: list[list[tuple[str, str]]] = []
    for server in servers:
        for city in cities:
            form_data.append(
                [
                    ("world", server.strip()),
                    ("town", city.strip()),
                    ("state", "auctioned"),
                    ("type", "houses"),
                    ("order", ""),
                ]
            )
    collected_data = await fetch_data(client, url_cities, form_data)
    result = []
    for response in collected_data:
        if response.status == 200:
            data = await response.text()
            result.extend(parse_houses(data))
        elif response.status == 403:
            continue
        else:
            raise NotAvailableElementError(
                f"Failed to fetch houses data, status code: {response.status}"
            )

    save_houses_to_file(result, "houses.csv")


if __name__ == "__main__":
    asyncio.run(main())
