"""
This script analyzes football player data to determine the most frequent shirt numbers
by position across different leagues. It provides two main functions:

1. get_top_shirts_by_position: Identifies the most frequent shirt numbers for a specified position.
2. getall_league_shirt_frequency: Aggregates the shirt number frequencies across all positions in a league.

The script can be executed directly to read data from a CSV file, process it, and save the results to a new CSV file.

Modules:
    pandas

Functions:
    get_top_shirts_by_position(df: pd.DataFrame, pos: str, n: int) -> list or tuple
        Returns a tuple or list of tuples of the most frequent shirt number(s) and their frequency for a given position.
        
    getall_league_shirt_frequency(league_df: pd.DataFrame, n: int) -> pd.DataFrame
        Aggregates and returns the shirt number frequencies across all positions in a league.

    main()
        The main function that reads data from 'scraped_data.csv', processes it, and saves the result to 'filename.csv'.

Constants:
    POSITION_DICT (dict): Mapping of position abbreviations to full position names.
    UEFA_TOP5_LEAGUE_NAMES (list): List of top 5 UEFA league names.
"""

import pandas as pd

POSITION_DICT = {
    "GK": "Goalkeeper",
    "CB": "Centre-Back",
    "LB": "Left-Back",
    "RB": "Right-Back",
    "DM": "Defensive Midfield",
    "CM": "Central Midfield",
    "AM": "Attacking Midfield",
    "LW": "Left Winger",
    "RW": "Right Winger",
    "SS": "Second Striker",
    "CF": "Centre-Forward",
}

UEFA_TOP5_LEAGUE_NAMES = [
    "Europe_top5",
    "Premier_League",
    "LaLiga",
    "Bundesliga",
    "Serie_A",
    "Ligue_1",
]


def get_top_shirts_by_position(df: pd.DataFrame, pos: str, n: int = 1):
    """
    Returns a tuple or list of tuples of the most frequent `n` shirt number(s) and their frequency for the given `position`.

    Args:
        df (pd.DataFrame): DataFrame containing player data.
        pos (str): Abbreviation of the player position.
        n (int): Number of top shirt numbers to return. Defaults to 1.

    Returns:
        list or tuple: A tuple or list of tuples containing position, shirt number, and frequency.
    """
    position = POSITION_DICT[pos]
    query = "position == @position"
    top_shirts_occurences = df.query(query)["shirt_no"].value_counts()[:n]
    if top_shirts_occurences.empty:
        return (pos, 0, 0)
    if n > 1:
        result = []
        for i in range(n):
            result.append(
                (pos, top_shirts_occurences.index[i], top_shirts_occurences.iloc[i])
            )
        return result
    else:
        shirt_no = top_shirts_occurences.index[0]
        frequency = top_shirts_occurences.iloc[0]
        return (pos, shirt_no, frequency)


def getall_league_shirt_frequency(league_df: pd.DataFrame, n: int = 1):
    """
    Aggregates and returns the shirt number frequencies across all positions in a league.

    Args:
        league_df (pd.DataFrame): DataFrame containing league data.
        n (int): Number of top shirt numbers to return for each position. Defaults to 1.

    Returns:
        pd.DataFrame: DataFrame containing positions, shirt numbers, and their frequencies.
    """
    league_data = [get_top_shirts_by_position(league_df, k, n) for k in POSITION_DICT]
    df = pd.DataFrame(league_data, columns=["position", "shirt_no", "frequency"])
    return df


def main():
    df = pd.read_csv("scraped_data.csv")  # Read the data csv from scraper as DataFrame
    data = getall_league_shirt_frequency(df)  # Apply the function to the df
    data.to_csv("filename.csv", index=False)  # Save df as csv, optional.


if __name__ == "__main__":
    main()
