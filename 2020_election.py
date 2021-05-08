import numpy as np
import pandas as pd
import seaborn as sns
import fire
import matplotlib.pyplot as plt
import plotly_express as px
from utils import *

def build_govenors_heatmap():
    '''construct data frames for each CSV and merge into one readable dataframe, subsequently rename columns, and resequence.
    Finally build a heat map using winning party numbers'''
    #set_pandas restrictions from utils
    set_pandas()
    #Building 3 seperate DataFrames based on State/County/candidate data
    gstate = pd.read_csv("/Users/agostinofante/Desktop/anthony-tino-datasets/archive/governors_state.csv")
    gcounties = pd.read_csv("/Users/agostinofante/Desktop/anthony-tino-datasets/archive/governors_county.csv")
    gcounties_can = pd.read_csv("/Users/agostinofante/Desktop/anthony-tino-datasets/archive/president_county_candidate.csv")

    #merge 3 DFs into 1
    merged_gdata = gcounties.merge(gcounties_can,how="left", on=["state","county"])
    merged_gdata = merged_gdata.merge(gstate,how="left", on="state")
    governors_df = merged_gdata

    #Copy Columns w/ Better Titles
    governors_df["state_total"] = governors_df["votes"]
    governors_df["county_candidate_reported"] = governors_df["current_votes"]
    governors_df["state_reported"] = governors_df["total_votes_x"]
    governors_df["county_total"] = governors_df["total_votes_y"]

    #Drop Irrelevant Columns
    governors_df.drop(columns=["total_votes_x", "current_votes", "votes", "total_votes_y"])
    #Set a variable for resequence
    cols = ["state", "county", "candidate", "party", "county_total", "county_candidate_reported", "state_reported", "state_total", "percent", "won"]
    #Call our resequence function to shuffle order based on what we want
    governors_df = resequence(governors_df,cols)

    #Build a list of non-numerical columns and use LabelEncoder library to assign binary numerical value
    strings = ["state", "candidate", "county", "party", "won"]
    #Call our Encoder function to hit the LabelEncoder
    #governors_df = Encoder(governors_df, strings)
    won_state = pd.pivot_table(governors_df,index=["state"],columns="won",values="party", fill_value=1,aggfunc=lambda x : len(x))
    sns.heatmap(won_state,annot=True,fmt=".0f",cmap="Greens")
    plt.show()
    return

def build_County_heatmap():
    ''''''
    #set_pandas restrictions from utils
    set_pandas()
    #Building DataFrames based on candidate data
    df_pres = pd.read_csv("/Users/agostinofante/Desktop/anthony-tino-datasets/archive/president_county_candidate.csv")
    #set party variables
    rep = df_pres['party'] == 'REP'
    dem = df_pres['party'] == 'DEM'
    df_pres = df_pres[rep|dem]
    #group by state &  party
    df_pres = df_pres.groupby(['state', 'party']).sum()
    df_pres = df_pres.unstack()
    df_pres = df_pres.reset_index()
    #load latitude & longitude file into a dataframe & take just the state & state code columns
    states = pd.read_csv("/Users/agostinofante/Desktop/anthony-tino-datasets/archive/latitude-and-longitude-for-every-country-and-state.csv")
    states = states[['usa_state', 'usa_state_code']]
    #merge states & pres data ###Important evaluate column names, the rename here converts back to strings as this often returns Tuple data types which will give key errors
    merged = df_pres.merge(states, left_on='state', right_on='usa_state')
    merged.rename(columns=''.join, inplace=True)
    #calculate percentage of Democrats based on the below equation and plot the data into the US plot
    merged['percent_democrat'] = merged['total_votesDEM']*100/(merged['total_votesREP']+merged['total_votesDEM'])
    fig = px.choropleth(merged,
                    locations="usa_state_code",
                    color = "percent_democrat",
                    locationmode = 'USA-states',
                    hover_name="state",
                    range_color=[25,75],
                    color_continuous_scale = 'RdBu',#blues
                    scope="usa",
                    title='2020 USA Election: Percent of Population Voting for the Democratic Party (as of +todays_date+)')
    fig.show()
    return

def build_Wash_map():
    '''Build Simple bar chart of Party choices specific to Washignton State'''
    set_pandas()
    df_pres = pd.read_csv("/Users/agostinofante/Desktop/anthony-tino-datasets/archive/president_county_candidate.csv")
    #set party variables
    rep = df_pres['party'] == 'REP'
    dem = df_pres['party'] == 'DEM'
    df_pres = df_pres[rep|dem]
    #select just columns where State == Washington
    Washginton = df_pres.loc[df_pres['state'] == 'Washington']
    #group df based on total votes & aggregate
    wash_votes = Washginton.groupby('party')['total_votes'].sum()
    fig = px.bar(wash_votes, title="2020 USA Election: Number of Votes per Party in Washington (Repulcian vs. Democrat)")
    fig.show()
    return

def build_US_votemap():
    '''Build a votemap of relevant Presiential Vote Counts by State'''
    set_pandas()
    df_pres = pd.read_csv("/Users/agostinofante/Desktop/anthony-tino-datasets/archive/president_state.csv")
    states = pd.read_csv("/Users/agostinofante/Desktop/anthony-tino-datasets/archive/latitude-and-longitude-for-every-country-and-state.csv")
    states = states[['usa_state', 'usa_state_code']]
    merged = df_pres.merge(states, left_on='state', right_on='usa_state')
    fig = px.choropleth(merged,
        locations="usa_state_code",
        color="total_votes",
        locationmode="USA-states",
        hover_name="state",
        range_color=[0,10000000],scope="usa",
        title="2020 USA Presiential Election Vote Counts"
    )
    fig.show()
    return


if __name__ == "__main__":
    '''Main function to run code'''
    fire.Fire()
