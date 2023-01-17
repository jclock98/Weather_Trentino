from get_locality_forecast import get_localities_forecasts
import json


def main():
    with open("localities.json", 'r') as fp:
        localities = json.load(fp)

    get_localities_forecasts(localities)


if __name__ == "__main__":
    main()