import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define URLs for each team
english_urls = {
    "Manchester United": "https://fbref.com/en/squads/19538871/Manchester-United-Stats"
}
belgian_urls = {
    "Genk": "https://fbref.com/en/squads/1e972a99/Genk-Stats"
}

# Function to fetch and display data
def fetch_and_display_data(url, team_name):
    if url:
        try:
            # Attempt to read tables from the URL
            tables = pd.read_html(url, header=1)
            if tables:
                # Display the primary table
                st.subheader(f"{team_name} - Stats")
                df = tables[0]  # Use the loaded table

                # Drop the last two rows from the DataFrame
                df = df[:-2]  # Keep all rows except the last two

                st.dataframe(df)

                # Call the plotting function for goal distribution
                plot_goal_distribution(df, team_name)
                st.markdown("---")
                plot_assits_distribution(df, team_name)
                st.markdown("---")
                plot_minutes_distribution(df, team_name)

            else:
                st.warning("No data tables found on this page.")
        except Exception as e:
            st.error(f"Error loading data for {team_name}: {e}")
    else:
        st.write("No data available for the selected team.")

# Define the plotting function for goal distribution
def plot_goal_distribution(df, team_name):
    # Ensure 'Player' and 'Gls' columns are in the data
    if 'Player' in df.columns and 'Gls' in df.columns:
        # Filter DataFrame for players with Gls > 0
        filtered_df = df[df['Gls'] > 0]

        if not filtered_df.empty:  # Check if the filtered DataFrame is not empty
            sorted_df = filtered_df.sort_values(by='Gls',ascending=False)

            fig, ax = plt.subplots()
            ax.bar(sorted_df['Player'], sorted_df['Gls'], color='skyblue')
            ax.set_xlabel('Player')
            ax.set_ylabel('Goals')
            ax.set_title(f"{team_name} - Goal Distribution by Player (Gls > 0)")
            plt.xticks(rotation=90)  # Rotate player names for readability
            st.pyplot(fig)
        else:
            st.warning("No players with goals greater than 0 found.")
    else:
        st.warning("Columns 'Player' or 'Gls' not found in the data.")

def plot_assits_distribution(df, team_name):
    # Ensure 'Player' and 'Gls' columns are in the data
    if 'Player' in df.columns and 'Ast' in df.columns:
        # Filter DataFrame for players with Gls > 0
        filtered_df = df[df['Ast'] > 0]

        if not filtered_df.empty:  # Check if the filtered DataFrame is not empty
            sorted_df = filtered_df.sort_values(by='Ast',ascending=False)

            fig, ax = plt.subplots()
            ax.bar(sorted_df['Player'], sorted_df['Ast'], color='skyblue')
            ax.set_xlabel('Player')
            ax.set_ylabel('Goals')
            ax.set_title(f"{team_name} - Assits Distribution by Player (Ast > 0)")
            plt.xticks(rotation=90)  # Rotate player names for readability
            st.pyplot(fig)
        else:
            st.warning("No players with goals greater than 0 found.")
    else:
        st.warning("Columns 'Player' or 'Gls' not found in the data.")


# Function to plot minutes distribution
def plot_minutes_distribution(df, team_name):
    if 'Player' in df.columns and 'Min' in df.columns:
        # Filter DataFrame for players who have played more than 0 minutes
        filtered_df = df[df['Min'] > 0]

        if not filtered_df.empty:
            sorted_df = filtered_df.sort_values(by='Min', ascending=True)

            fig, ax = plt.subplots()
            ax.barh(sorted_df['Player'], sorted_df['Min'], color='lightgreen')
            ax.set_xlabel('Minutes Played')
            ax.set_ylabel('Player')
            ax.set_title(f"{team_name} - Minutes Played by Player")
            st.pyplot(fig)
        else:
            st.warning("No players with minutes played found.")
    else:
        st.warning("Columns 'Player' or 'Min' not found in the data.")



# Sidebar for league selection
selected_league = st.sidebar.selectbox("Choose a League", ["Belgian Pro", "English Premier League"])

# Team selection and data display based on chosen league
if selected_league == "English Premier League":
    selected_team = st.sidebar.selectbox("Choose a Team", list(english_urls.keys()))
    fetch_and_display_data(english_urls.get(selected_team), selected_team)

elif selected_league == "Belgian Pro":
    selected_team = st.sidebar.selectbox("Choose a Team", list(belgian_urls.keys()))
    fetch_and_display_data(belgian_urls.get(selected_team), selected_team)

else:
    st.write("No league data is currently available.")
