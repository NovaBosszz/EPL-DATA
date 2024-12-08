import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define URLs for each team
english_urls = {
    "Manchester United": "https://fbref.com/en/squads/19538871/Manchester-United-Stats",
    "Liverpool": "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
    "Arsenal":"https://fbref.com/en/squads/18bb7c10/Arsenal-Stats"
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
                df = tables[0]
                df = df[:-2]  # Drop the last two rows

                st.dataframe(df)

                # Call the plotting function for each metric
                plot_metric_distribution(df, team_name, "Gls", "Goals")
                st.markdown("---")
                plot_metric_distribution(df, team_name, "Ast", "Assists")
                st.markdown("---")
                plot_minutes_distribution(df, team_name)
                st.markdown("---")
                plot_goals_assists_per_90(df, team_name)

            else:
                st.warning("No data tables found on this page.")
        except Exception as e:
            st.error(f"Error loading data for {team_name}: {e}")
    else:
        st.write("No data available for the selected team.")

# Generalized function to plot distributions (Goals/Assists)
def plot_metric_distribution(df, team_name, metric, metric_label):
    if 'Player' in df.columns and metric in df.columns:
        filtered_df = df[df[metric] > 0].sort_values(by=metric, ascending=False)

        if not filtered_df.empty:
            fig, ax = plt.subplots()
            sns.barplot(y="Player", x=metric, data=filtered_df, palette="viridis", ax=ax)
            ax.set_xlabel(metric_label)
            ax.set_ylabel('Player')
            ax.set_title(f"{team_name} - {metric_label} Distribution by Player ({metric_label} > 0)")
            st.pyplot(fig)
        else:
            st.warning(f"No players with {metric_label.lower()} greater than 0 found.")
    else:
        st.warning(f"Columns 'Player' or '{metric}' not found in the data.")

# Function to plot minutes distribution
def plot_minutes_distribution(df, team_name):

    if 'Player' in df.columns and 'Min' in df.columns:
        filtered_df = df[df['Min'] > 0].sort_values(by='Min', ascending=True)

        if not filtered_df.empty:
            fig, ax = plt.subplots()
            sns.barplot(x="Min", y="Player", data=filtered_df, palette="Blues_r", ax=ax)
            ax.set_xlabel('Minutes Played')
            ax.set_ylabel('Player')
            ax.set_title(f"{team_name} - Minutes Played by Player")
            st.pyplot(fig)
        else:
            st.warning("No players with minutes played found.")
    else:
        st.warning("Columns 'Player' or 'Min' not found in the data.")

# Function Goals and Assists per 90 Minute
def plot_goals_assists_per_90(df, team_name):
    # Ensure necessary columns are present
    if 'Player' in df.columns and 'Gls' in df.columns and 'Ast' in df.columns and '90s' in df.columns and 'Min' in df.columns and 'Starts' in df.columns:
        # Calculate the 50% starting threshold based on the maximum starts
        max_starts = df['Starts'].max()
        threshold_starts = max_starts * 0.25

        # Filter for regular starters, and for players with > 0 goals, > 0 assists, and significant playing time (Min >= 90)
        filtered_df = df[(df['Starts'] >= threshold_starts) & (df['Gls'] > 0) & (df['Ast'] > 0) & (df['Min'] >= 90)]

        # Calculate goals and assists per 90 minutes
        filtered_df['Gls/90'] = filtered_df['Gls'] / filtered_df['90s']
        filtered_df['Ast/90'] = filtered_df['Ast'] / filtered_df['90s']

        if not filtered_df.empty:  # Check if filtered DataFrame is not empty
            # Create the scatter plot
            fig, ax = plt.subplots()
            ax.scatter(filtered_df['Ast/90'], filtered_df['Gls/90'], color='teal')

            # Determine median values for categorization
            median_gls90 = filtered_df['Gls/90'].median()
            median_ast90 = filtered_df['Ast/90'].median()

            # Define a threshold to include players just below the median
            gls_threshold = median_gls90 * 0.8  # For example, consider 80% of the median
            ast_threshold = median_ast90 * 0.8

            # Separate players based on categories
            top_right = filtered_df[(filtered_df['Gls/90'] > median_gls90) & (filtered_df['Ast/90'] > median_ast90)]
            upper = filtered_df[(filtered_df['Gls/90'] > median_gls90) & (filtered_df['Ast/90'] <= ast_threshold)]
            right = filtered_df[(filtered_df['Ast/90'] > median_ast90) & (filtered_df['Gls/90'] <= gls_threshold)]
            close_upper = filtered_df[(filtered_df['Gls/90'] > gls_threshold) & (filtered_df['Ast/90'] <= median_ast90)]
            close_right = filtered_df[(filtered_df['Ast/90'] > ast_threshold) & (filtered_df['Gls/90'] <= median_gls90)]

            # Add player annotations and median lines
            for i, player in filtered_df.iterrows():
                ax.text(player['Ast/90'], player['Gls/90'], player['Player'], fontsize=8, ha='left')

            ax.axhline(median_gls90, color='gray', linestyle='--', linewidth=0.5, label='Median Gls/90')
            ax.axvline(median_ast90, color='gray', linestyle='--', linewidth=0.5, label='Median Ast/90')

            # Set labels and title
            ax.set_xlabel('Assists per 90 Minutes')
            ax.set_ylabel('Goals per 90 Minutes')
            ax.set_title(f"{team_name} - Goals and Assists per 90 Minutes (Min >= 90)")

            # Display the plot
            st.pyplot(fig)

            # Display players by category below the plot
            st.markdown("### Player Categories")
            reported_players = set()  # To keep track of reported players

            # Use Streamlit's columns to display categories in a more compact, side-by-side layout.
            col1, col2, col3, col4, col5 = st.columns(5)

            # Define a helper function for displaying in each column
            def display_category_in_column(column, title, df):
                """Displays a category list in a specific Streamlit column."""
                with column:
                    st.markdown(f"**{title}:**")
                    if not df.empty:
                        for idx, player in enumerate(df['Player'].tolist(), start=1):
                            if player not in reported_players:
                                st.markdown(f"{idx}. {player}")
                                reported_players.add(player)
                    else:
                        st.markdown("None")

            # Display each category in separate columns
            display_category_in_column(col1, "Well-rounded offensive players (High Gls/90 and Ast/90)", top_right)
            display_category_in_column(col2, "Primarily scorers (High Gls/90, just below Ast/90 median)", upper)
            display_category_in_column(col3, "Primarily assist-makers (High Ast/90, just below Gls/90 median)", right)
            display_category_in_column(col4, "Close to Primarily scorers (High Gls/90)", close_upper)
            display_category_in_column(col5, "Close to Primarily assist-makers (High Ast/90)", close_right)























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
