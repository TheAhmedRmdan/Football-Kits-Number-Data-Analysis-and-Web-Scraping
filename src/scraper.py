"""
A web scraper for transfermarkt.com to get players' names, positions, and shirt numbers.
`headers` are a dictionary containing User-Agent data, must be used to scrape transfermarkt
because they block any python requests.

Modules:
    requests
    bs4 (BeautifulSoup)
    csv

Functions:
    get_league_teams_urls(league_url: str, headers: dict, season: int = 2023) -> list
        Get links to all teams of a certain league given its URL as input. Returns a list of URLs.
        
    get_squad_data(team_url: str, headers: dict) -> list
        Gets a team's player data given team URL as input. Returns a list of tuples (name, position, shirt number).
        
    get_all_league_squads_info(league_url: str, headers: dict, season: int = 2023) -> list
        Applies get_squad_data() to all league teams given the league URL as input. Returns a list of lists containing all the league's player data.
        
    write_league_data_to_csv(league_data: list, league_name: str) -> None
        Convert the league(s) data to a CSV file given the league data and league name. Writes a CSV file to the current directory named under the league's name.
        
    main() -> None
        The main function that sets headers and league URLs, then scrapes data for the leagues and saves them as CSV files.
"""

import requests
from bs4 import BeautifulSoup
import csv


def get_league_teams_urls(league_url, headers, season=2023):
    """
    Get links to all teams of a certain league given its URL as input.

    Args:
        league_url (str): URL of the league.
        headers (dict): Dictionary containing User-Agent data.
        season (int): Season year. Defaults to 2023.

    Returns:
        list: List containing the URLs of the teams in the league.
    """
    if "?saison_id=" not in league_url:
        league_url = league_url + f"/plus/?saison_id={season}"
    league_response = requests.get(league_url, headers=headers)
    league_soup = BeautifulSoup(league_response.text, "lxml")
    league_teams = league_soup.find_all("td", class_="hauptlink no-border-links")
    urls = [team.find("a").get("href") for team in league_teams]
    urls = ["".join(["https://www.transfermarkt.com", url]) for url in urls]
    return urls


def get_squad_data(team_url, headers):
    """
    Gets a team's player data given team URL as input.

    Args:
        team_url (str): URL of the team.
        headers (dict): Dictionary containing User-Agent data.

    Returns:
        list: List of tuples (name, position, shirt number).
    """
    squad_info = []
    team_response = requests.get(team_url, headers=headers)
    team_soup = BeautifulSoup(team_response.text, "lxml")
    squad_table = team_soup.find("table", class_="items")
    players = squad_table.find_all("td", class_="posrela")
    number_rows = team_soup.find_all("div", class_="rn_nummer")
    numbers = [row.text for row in number_rows]
    numbers.reverse()
    for player in players:
        name = player.find("td", class_="hauptlink").text.strip()
        position = player.find_all("td")[-1].text.strip()
        shirt_num = numbers.pop()
        squad_info.append(tuple([name, position, shirt_num]))
    return squad_info


def get_all_league_squads_info(league_url, headers, season=2023):
    """
    Applies get_squad_data() to all league teams given the league URL as input.

    Args:
        league_url (str): URL of the league.
        headers (dict): Dictionary containing User-Agent data.
        season (int): Season year. Defaults to 2023.

    Returns:
        list: List of lists containing all the league's player data.
    """
    league_links = get_league_teams_urls(league_url, headers, season)
    all_league_squads = []
    for team in league_links:
        try:
            print("Processing team at url: ", team)
            team_info = get_squad_data(team, headers)
            print("Processing done")
        except Exception as err:
            print("Error: ", err)
        all_league_squads.append(team_info)
    return all_league_squads


def write_league_data_to_csv(league_data, league_name):
    """
    Convert the league(s) data to a CSV file given the league data and league name.

    Args:
        league_data (list): List of lists containing player data for the league.
        league_name (str): Name of the league.

    Writes:
        A CSV file to the current directory named under the league's name.
    """
    with open(f"{league_name}.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "position", "shirt_no"])
        for team_data in league_data:
            writer.writerows(team_data)


def main():
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }
    EUROPE_TOP_5_LEAGUES = {
        "Premier_League": "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1",
        "LaLiga": "https://www.transfermarkt.com/primera-division/startseite/wettbewerb/ES1",
        "Bundesliga": "https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1",
        "Serie_A": "https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1",
        "Ligue_1": "https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1",
    }
    # Usage Example: Scrape Europe top 5 leagues, and save them as separate csv files
    for league_name, link in EUROPE_TOP_5_LEAGUES.items():
        write_league_data_to_csv(get_all_league_squads_info(link, HEADERS), league_name)
        print(league_name + " ######### Finished ######### ")


if __name__ == "__main__":
    main()
