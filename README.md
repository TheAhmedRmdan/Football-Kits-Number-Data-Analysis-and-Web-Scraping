# Football Kits Number Data Analysis and Web Scraping Project
![eutop5](https://github.com/TheAhmedRmdan/Football-Kits-Number-Data-Analysis-and-Web-Scraping/assets/61194549/da336478-b745-4127-80b2-900c7d9d8f8a)
![Egy](https://github.com/TheAhmedRmdan/Football-Kits-Number-Data-Analysis-and-Web-Scraping/assets/61194549/0e725902-2412-42d5-bc1f-b9393721887b)
## Project Overview

This project involves two main components:
1. **Data Analysis**: Analyzing football player data to determine the most frequent shirt numbers by position across different leagues.
2. **Web Scraping**: Scraping player data from Transfermarkt.com to collect player names, positions, and shirt numbers.

## Project Structure

The project contains the following Python scripts:
1. `analysis.py`: This script analyzes player data to determine the most frequent shirt numbers by position.
2. `scraper.py`: This script scrapes player data from Transfermarkt.com.

## Requirements

- Python 3.x
- pandas
- requests
- BeautifulSoup4
- lxml

You can install the required libraries using pip:
```sh
pip install pandas requests beautifulsoup4 lxml
```

## Usage

### 1. Data Analysis (`analysis.py`)

This script processes a CSV file containing player data and determines the most frequent shirt numbers by position.

#### Functions

- `get_top_shirts_by_position(df: pd.DataFrame, pos: str, n: int = 1) -> list or tuple`: Returns the most frequent `n` shirt number(s) and their frequency for a given position.
- `getall_league_shirt_frequency(league_df: pd.DataFrame, n: int = 1) -> pd.DataFrame`: Aggregates the shirt number frequencies across all positions in a league.
- `main()`: The main function that reads data from 'scraped_data.csv', processes it, and saves the result to 'filename.csv'.


### 2. Web Scraping (`scraper.py`)

This script scrapes player data from Transfermarkt.com, including player names, positions, and shirt numbers.

#### Functions

- `get_league_teams_urls(league_url: str, headers: dict, season: int = 2023) -> list`: Get links to all teams of a certain league given its URL as input.
- `get_squad_data(team_url: str, headers: dict) -> list`: Gets a team's player data given team URL as input.
- `get_all_league_squads_info(league_url: str, headers: dict, season: int = 2023) -> list`: Applies `get_squad_data()` to all league teams given the league URL as input.
- `write_league_data_to_csv(league_data: list, league_name: str) -> None`: Convert the league(s) data to a CSV file given the league data and league name.
- `main()`: The main function that sets headers and league URLs, then scrapes data for the leagues and saves them as CSV files.


This will scrape data for the specified leagues and save them as CSV files in the current directory.

## Notes

- Ensure you have a stable internet connection while running `scraper.py` as it fetches data from Transfermarkt.com.
- Modify the URLs and headers in the `main()` function of `scraper.py` as needed to scrape data for different leagues or seasons.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
