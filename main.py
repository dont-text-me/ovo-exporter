import asyncio
from fetch.fetch import fetch_last_three_days
from export.export import export_readings


def main():
    readings = asyncio.run(fetch_last_three_days())
    export_readings(readings)


if __name__ == "__main__":
    main()
