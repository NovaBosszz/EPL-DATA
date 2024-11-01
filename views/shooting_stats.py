import streamlit as st 
import requests 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px
from adjustText import adjust_text




st.title("Football Shooting Stats")

# Define URLs for different leagues
urls = {
   
    "Belgian Pro League": "https://fbref.com/en/comps/37/shooting/Belgian-Pro-League-Stats#all_stats_shooting",
    "Premier League": "https://fbref.com/en/comps/9/shooting/Premier-League-Stats#all_stats_shooting",

}

# Dropdown menu for selecting league
selected_league = st.selectbox("Select a League", list(urls.keys()))

# Load data from the selected URL
url = urls[selected_league]
st.subheader(f"Loading data from: **{selected_league}**")


#Loading Data from the url
pd.set_option('display.max_columns', None)
html = pd.read_html(url, header=1)
df = html[0]

#raw dataframe
#st.dataframe(df)

#Rename Columns for Readability 
df.rename(columns = {
    "# Pl": "no_players",
    "90s": "no_matches",
    }, inplace=True)

# Display Dataframe in an interactive table....Clean dataframe
st.dataframe(df)
st.markdown("---")

def plot_team_goals(df):
    st.header('League Goals Scored By Teams')

    # Group by 'Squad' and 'passes_Cmp' and 'passes_Att'

    league_goals = df[['Squad','Gls']].sort_values( by='Gls', ascending=False)
                                        
    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    league_goals.plot(kind="bar", x='Squad', y=['Gls'], ax =ax , color=['#1f77b4'])

    ax.set_title('League Goals Scored By Teams')
    ax.set_ylabel('Number of Goals')
    ax.set_xlabel('Squad')
    ax.set_xticklabels(league_goals['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 6), 
                    textcoords='offset points', fontsize=8)

    st.pyplot(fig)

def plot_team_goals_scatter(df):
    # Check if the required columns are present
    if not {'xG', 'Gls', 'Squad'}.issubset(df.columns):
        st.error("Dataframe missing one of the required columns: 'xG', 'Gls', or 'Squad'")
        return
    
    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = ax.scatter(df['xG'], df['Gls'], alpha=0.6, s=100)

    # Add labels and title
    ax.set_xlabel('Expected Goals (xG)', fontsize=12)
    ax.set_ylabel('Actual Goals (Gls)', fontsize=12)
    ax.set_title('Actual Goals vs Expected Goals', fontsize=14)

    # Add a diagonal line for reference (xG = Gls)
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
    ]
    ax.plot(lims, lims, 'r--', alpha=0.75, zorder=0)

    # Add team labels to points
    texts = [
        ax.text(df['xG'].iloc[i], df['Gls'].iloc[i], txt, fontsize=18, alpha=0.7)
        for i, txt in enumerate(df['Squad'])
    ]

    # Adjust text to minimize overlap
    adjust_text(texts, arrowprops=dict(arrowstyle="-", color='gray', lw=0.5))

    # Adjust layout to prevent clipping of tick-labels and display in Streamlit
    fig.tight_layout()
    st.pyplot(fig)
    
def plot_team_shots(df):
    st.header('Shots Vs Shots On Target By Teams')

    # Group by 'Squad' and 'Shots' and 'Shots On Target'

    league_shots = df[['Squad','SoT', 'Sh']].sort_values( by='Sh', ascending=False)
                                        
    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    league_shots.plot(kind="bar", x='Squad', y=['SoT', 'Sh'], ax =ax , color=['#1f77b4', '#ff7f0e'])

    ax.set_title('League Goals Scored By Teams')
    ax.set_ylabel('Number of Goals')
    ax.set_xlabel('Squad')
    ax.set_xticklabels(league_shots['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    st.pyplot(fig)

# Calling functions to generate each plot

if df is not None:
    plot_team_goals(df)     
    st.markdown("---")
    plot_team_goals_scatter(df)
    st.markdown("---")
    plot_team_shots(df)
    st.markdown("---")