import numpy as np
import pandas as pd
from typing import Union

pd.options.mode.chained_assignment = None

def medal_tally(df: pd.DataFrame) -> Union[list, list]:
    medal_tally = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally = medal_tally.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending=False).reset_index()
    medal_tally["total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
    
    # convert to integer
    medal_tally["Gold"] = medal_tally["Gold"].astype("int")
    medal_tally["Silver"] = medal_tally["Silver"].astype("int")
    medal_tally["Bronze"] = medal_tally["Bronze"].astype("int")
    medal_tally["total"] = medal_tally["total"].astype("int")
    return medal_tally


def countries_year_list(df: pd.DataFrame):
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    countries = np.unique(df["region"].dropna().values).tolist()
    countries.sort()
    countries.insert(0, "Overall")
    return years, countries


def fetch_medal_tally(df: pd.DataFrame, year: Union[int, str], country: str) -> pd.DataFrame:
    flag = 0
    medal_df = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    elif year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    elif year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == year]
    else:
        temp_df = medal_df[(medal_df["Year"] == year) & (medal_df["region"] == country)]
    
    if flag == 1:
        x = temp_df.groupby("Year").sum()[["Gold", "Silver", "Bronze"]].sort_values("Year", ascending=True).reset_index()
        x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]
    else:
        x = temp_df.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending=False).reset_index()
        x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]

        # convert to integer
        x["Gold"] = x["Gold"].astype("int")
        x["Silver"] = x["Silver"].astype("int")
        x["Bronze"] = x["Bronze"].astype("int")
        x["total"] = x["total"].astype("int")
    
    return x


def data_over_time(df: pd.DataFrame, column: str) -> pd.DataFrame:
    nations_over_time = df.drop_duplicates(["Year", column])["Year"].value_counts().reset_index().sort_values("index")
    nations_over_time.rename(columns = {"index": "Edition", "Year": column}, inplace=True)
    return nations_over_time


def most_successful(df: pd.DataFrame, sport: str) -> pd.DataFrame:
    temp_df = df.dropna(subset=["Medal"])
    
    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]
    temp_df = temp_df["Name"].value_counts().reset_index().head(15).merge(df, left_on="index", right_on="Name", how="left")
    x = temp_df[["index", "Name_x", "Sport", "region"]].drop_duplicates("index")
    x.rename(columns = {"index": "Name", "Name_x": "Medals"}, inplace = True)
    return x

def year_wise_medal_tally(df: pd.DataFrame, country: str) -> pd.DataFrame:
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)
    new_df   = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()
    return final_df

def country_event_heatmap(df: pd.DataFrame, country: str) -> pd.DataFrame:
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)
    new_df   = temp_df[temp_df["region"] == country]
    pivot_table = new_df.pivot_table(index="Sport", columns="Year", values="Medal", aggfunc="count").fillna(0)
    return pivot_table

def most_successful_country_wise(df: pd.DataFrame, country: str) -> pd.DataFrame:
    temp_df = df.dropna(subset=["Medal"])
    
    
    temp_df = temp_df[temp_df["region"] == country]
    
    temp_df = temp_df["Name"].value_counts().reset_index().head(15).merge(df, left_on="index", right_on="Name", how="left")
    x = temp_df[["index", "Name_x", "Sport"]].drop_duplicates("index")
    x.rename(columns = {"index": "Name", "Name_x": "Medals"}, inplace = True)
    return x

def weight_vs_height(df: pd.DataFrame, sport: str) -> pd.DataFrame:
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    athlete_df["Medal"].fillna("No Medal", inplace=True)

    if sport != "Overall":
        temp_df = athlete_df[athlete_df["Sport"] == sport]
    else:
        temp_df = athlete_df

    return temp_df

def men_vs_women(df: pd.DataFrame) -> pd.DataFrame:
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    men   = athlete_df[athlete_df["Sex"] == "M"].groupby("Year").count()["Name"].reset_index()
    women = athlete_df[athlete_df["Sex"] == "F"].groupby("Year").count()["Name"].reset_index()

    final = men.merge(women, on="Year", how="left").fillna(0)
    final.rename(columns={"Name_x":"Male", "Name_y":"Female"}, inplace=True)
    return final
