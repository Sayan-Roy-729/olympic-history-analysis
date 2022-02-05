import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

import preprocessor
import helper

pd.options.mode.chained_assignment = None

# import our datasets 
df        = pd.read_csv("./Dataset/athlete_events.csv")
region_df = pd.read_csv("./Dataset/noc_regions.csv")

df = preprocessor.preprocess(df, region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://stillmed.olympics.com/media/Images/OlympicOrg/IOC/The_Organisation/The-Olympic-Rings/Olympic_rings_TM_c_IOC_All_rights_reserved_1.jpg")

user_menu = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete wise Analysis")
)

if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")

    years, countries = helper.countries_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)

    if selected_year != "Overall":
        selected_year = int(selected_year)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    elif selected_year != "Overall" and selected_country == "Overall":
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == "Overall" and selected_country != "Overall":
        st.title(f"{selected_country} overall performance")
    else:
        st.title(f"{selected_country} performance in {selected_year} Olympics")

    st.table(medal_tally)


elif user_menu == "Overall Analysis":
    editions = df["Year"].unique().shape[0] - 1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]

    st.title("Top Statistics")

    col1, col2,  col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2,  col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    
    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athletes)

    # display graph of  Participating Nations over the years
    nations_over_time = helper.data_over_time(df, "region")
    fig = px.line(nations_over_time, x = "Edition", y = "region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    # display graph of  Participating Nations over the years
    events_over_time = helper.data_over_time(df, "Event")
    fig = px.line(events_over_time, x = "Edition", y = "Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    # display graph of  Participating Nations over the years
    athelets_over_time = helper.data_over_time(df, "Name")
    fig = px.line(athelets_over_time, x = "Edition", y = "Name")
    st.title("Athelets over the years")
    st.plotly_chart(fig)

    # No. of Events over time (Every Sport)
    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize = (16, 16))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int"), annot=True, ax=ax)
    st.pyplot(fig)

    st.title("Most 15 successful Athletes")
    # create user input dropdown to select sport type
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Select a Sport", sport_list)
    # display that filtered dataset
    x = helper.most_successful(df, selected_sport)
    st.table(x)

elif user_menu == "Country-wise Analysis":
    st.sidebar.title("Country-wise Analysis")

    # dropdown list of all countries participated into Olympics
    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a country", country_list)
    # filtered dataframe according to user selected dropdown value
    country_df = helper.year_wise_medal_tally(df, selected_country)
    # display a graph of medal tally over the years of that selected country
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(f"{selected_country} Medal Tally over the years")
    st.plotly_chart(fig)

    # display the events of that country over the years as heatmap
    st.title(f"{selected_country} excels in the following sports")
    pivot_table = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize = (16, 16))
    sns.heatmap(pivot_table, annot=True, ax=ax)
    st.pyplot(fig)

    # Displaoy most successful 15 Athelets country wise
    st.title(f"Top 15 athletes of {selected_country}")
    top15_df = helper.most_successful_country_wise(df, selected_country)
    st.table(top15_df)

### Athlete wise Analysis ###
else:
    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()

    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ["Overall Age", "Gold Medalist", "Silver Medalist", "Brownze Medalist"],
        show_hist=False,
        show_rug=False
    )
    fig.update_layout(autosize=False, width=1000, height=600)

    st.title("Distribution of Age")
    st.plotly_chart(fig)


    # famous sports distribution
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    x    = []
    name = []

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna())
        name.append(sport)
        
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    

    st.title("Distribution of Age wrt Sports of Gold Medalist")
    st.plotly_chart(fig)

    #####################################
    ### display height vs weight plot ###
    #####################################
    # fetch all sports
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.sidebar.selectbox("Select a Sport", sport_list)
    # display the sports dropdown list to select
    temp_df = helper.weight_vs_height(df, selected_sport)
    # create the graph
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.scatterplot(x=temp_df["Weight"], y=temp_df["Height"], hue=temp_df["Medal"], style=temp_df["Sex"], s=60, ax=ax)

    # display the graph
    st.title("Height vs Weight")
    st.pyplot(fig)

    ################################################
    #    display men vs women participate graph    #
    ################################################
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)

    st.title("Men vs Women Participation Over the Years")
    st.plotly_chart(fig)


