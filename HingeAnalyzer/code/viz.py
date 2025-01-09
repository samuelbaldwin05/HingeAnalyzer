import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import linregress
from code.sankey import make_sankey

# Functions for graphing
def main_stats(df):
    ''' Function to gather and display important stats from the matches dataframe
    '''
    total_likes_received = len(df[df['like_type'] == 'recieved'])

    # Total matches from received likes
    total_matches_from_received_likes = len(
        df[(df['like_type'] == 'recieved') & (df['match_type'] == 'match')]
    )
    percent_matches_from_received_likes = (
        (total_matches_from_received_likes / total_likes_received * 100)
        if total_likes_received > 0 else 0
    )

    # Total likes sent
    total_likes_sent = len(df[df['like_type'] == 'sent'])

    # Total matches from sent likes
    total_matches_from_sent_likes = len(
        df[(df['like_type'] == 'sent') & (df['match_type'] == 'match')]
    )
    percent_matches_from_sent_likes = (
        (total_matches_from_sent_likes / total_likes_sent * 100)
        if total_likes_sent > 0 else 0
    )

    # Overall totals
    total_likes = total_likes_received + total_likes_sent
    total_matches = len(df[df['match_type'] == 'match'])
    percent_matches_from_total_likes = (
        (total_matches / total_likes * 100) if total_likes > 0 else 0
    )

    percent_likes_recieved = (total_likes_received / total_likes) * 100
    percent_likes_sent = (total_likes_sent / total_likes) * 100

    # Other interesting stats
    total_messages = df['num_messages'].sum()
    avg_messages_per_match = total_messages / total_matches
    total_voice_notes = df['num_voice_notes'].sum()
    total_met = df[(df['met'].notna()) & (df['met'] != 'Not yet')].shape[0]


    df['like_timestamp'] = pd.to_datetime(df['like_timestamp'])
    min_timestamp = df['like_timestamp'].min()
    max_timestamp = df['like_timestamp'].max()

    date_diff = (max_timestamp - min_timestamp).days

    avg_likes_sent = total_likes_sent / date_diff
    avg_likes_received = total_likes_received / date_diff
    avg_matches = total_matches / date_diff

    # Display the results
    st.markdown("### Likes and Matches Statistics")
    st.write(f"**Total Likes (Sent + Received):** {total_likes}")
    st.write(f"**Total Matches:** {total_matches} (Match Percentage {percent_matches_from_total_likes:.2f}%)")
    st.markdown("")
    st.write(f"**Likes Received:** {total_likes_received} (Percent of Total Likes: {percent_likes_recieved:.2f}%)")
    st.write(f"**Matches from Received Likes:** {total_matches_from_received_likes} (Match Percentage: {percent_matches_from_received_likes:.2f}%)")
    st.markdown("")
    st.write(f"**Likes Sent:** {total_likes_sent} (Percent of Total Likes {percent_likes_sent:.2f}%)")
    st.write(f"**Matches from Sent Likes:** {total_matches_from_sent_likes} (Match Percentage: {percent_matches_from_sent_likes:.2f}%)")
    st.markdown("")
    st.markdown("### Other Statistics")
    st.write(f"**Total Messages (Sent + Recieved):** {total_messages}")
    st.write(f"**Average Number of Messages Per Match:** {avg_messages_per_match:.2f}")
    st.write(f"**Total Voice Notes (Sent):** {total_voice_notes}")
    st.write(f"**Total Matches Met:** {total_met}")
    st.write(f"**Average Likes Sent Per Day:** {avg_likes_sent:.2f}")
    st.write(f"**Average Likes Received Per Day:** {avg_likes_received:.2f}")
    st.write(f"**Average Matches Per Day:** {avg_matches:.2f}")
    st.markdown(f"<p style='font-size:14px;'>All averages are based on days between first and last like ({date_diff:.0f} days)</p>", unsafe_allow_html=True)
    st.markdown('---')

def plot_message_distribution(df):
    ''' Given the matches dataframe, displays a histplot of the 
    distrubtion of the number of messages for each interaction
    '''
    fig, ax = plt.subplots()
    sns.histplot(df['num_messages'], kde=True, ax=ax)
    ax.set_title('Distribution of Number of Messages')
    ax.set_xlabel('Number of Messages')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

def plot_avg_time_between_messages(df):
    ''' Given the matches dataframe, displays a histplot of 
    the distribution of the average time between messages for each interaction
    '''
    fig, ax = plt.subplots()
    sns.histplot(df['avg_time_between_messages'].dropna() / 3600, kde=True, ax=ax) 
    ax.set_title('Distribution of Average Time Between Messages')
    ax.set_xlabel('Average Time Between Messages (hours)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

def plot_avg_message_length(df):
    ''' Given the matches dataframe, displays a histplot of
    the distribution of the average message length (words/message) for each interaction
    '''
    fig, ax = plt.subplots()
    sns.histplot(df['avg_message_length'], kde=True, ax=ax)
    ax.set_title('Distribution of Average Message Length')
    ax.set_xlabel('Average Message Length (words)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

def plot_time_between_first_and_last_message(df):
    fig, ax = plt.subplots()
    sns.histplot(df['time_between_first_and_last_message'].dropna() / 3600, kde=True, ax=ax)  # Convert seconds to hours
    ax.set_title('Time Between First and Last Message')
    ax.set_xlabel('Time Between First and Last Message (hours)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

def plot_corr_messages_and_avg_time(df):
    filtered_df = df.dropna(subset=['num_messages', 'avg_time_between_messages'])
    fig, ax = plt.subplots()
    sns.scatterplot(x=filtered_df['num_messages'], y=filtered_df['avg_time_between_messages'], ax=ax)

    # Line of best fit
    slope, intercept, r_value, p_value, std_err = linregress(filtered_df['num_messages'], filtered_df['avg_time_between_messages'])
    line_x = filtered_df['num_messages']
    line_y = slope * line_x + intercept
    ax.plot(line_x, line_y, color='red', linestyle='--', label='Best Fit Line')

    r_squared = r_value**2
    ax.text(0.95, 0.95, f'R² = {r_squared:.2f}', horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontsize=12)

    ax.set_title('Correlation: Number of Messages vs Avg Time Between Messages')
    ax.set_xlabel('Number of Messages')
    ax.set_ylabel('Average Time Between Messages (seconds)')
    st.pyplot(fig)

def plot_time_between_like_and_match(df):
    if 'time_between_like_and_match' in df.columns:
        # Convert the column to hours
        df['time_between_like_and_match_hours'] = df['time_between_like_and_match'] / 3600  # Convert seconds to hours

        # Get the range of values
        min_val = float(df['time_between_like_and_match_hours'].min())
        max_val = float(df['time_between_like_and_match_hours'].max())

        st.markdown("---")
        # Add the slider to filter
        percentage_limit = st.slider(
            'Show Percentage of Maximum Time',
            min_value=0,
            max_value=100,
            value=100,
            step=1
        )

        # Calculate the upper limit based on the percentage
        upper_limit = (percentage_limit / 100) * max_val

        # Filter the data based on the percentage limit
        filtered_df = df[df['time_between_like_and_match_hours'] <= upper_limit]

        # Plot the filtered data
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(filtered_df['time_between_like_and_match_hours'].dropna(), kde=True, ax=ax)
        ax.set_title('Filtered Time Between Like and Match')
        ax.set_xlabel('Time Between Like and Match (hours)')
        ax.set_ylabel('Frequency')

        st.pyplot(fig)

        # Add a divider below the slider
        st.markdown("---")


def plot_likes_over_time(df):
    df['like_timestamp'] = pd.to_datetime(df['like_timestamp'])
    df['like_date'] = df['like_timestamp'].dt.date
    likes_per_day = df.groupby('like_date').size().cumsum()  # Cumulative sum of likes over time

    fig, ax = plt.subplots()
    likes_per_day.plot(kind='line', ax=ax, marker='o')
    ax.set_title('Likes Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Likes')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

def plot_matches_over_time(df):
    df['match_timestamp'] = pd.to_datetime(df['match_timestamp'])
    df['match_date'] = df['match_timestamp'].dt.date
    matches_per_day = df.groupby('match_date').size().cumsum()  # Cumulative sum of matches over time

    fig, ax = plt.subplots()
    matches_per_day.plot(kind='line', ax=ax)
    ax.set_title('Matches Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Matches')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

def plot_matches_by_weekday(df):
    # Ensure the timestamp is in datetime format
    df['match_timestamp'] = pd.to_datetime(df['match_timestamp'])
    # Extract weekday
    df['weekday'] = df['match_timestamp'].dt.day_name()

    # Count matches by weekday
    weekday_match_counts = df.groupby('weekday').size().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    # Plot matches by weekday
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=weekday_match_counts.index, y=weekday_match_counts.values, ax=ax)
    ax.set_title('Matches by Day of Week')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Number of Matches')
    st.pyplot(fig)

def plot_likes_and_matches_over_time(df):
    # Convert timestamps to datetime
    df['like_timestamp'] = pd.to_datetime(df['like_timestamp'])
    df['match_timestamp'] = pd.to_datetime(df['match_timestamp'])

    # Extract dates for grouping
    df['like_date'] = df['like_timestamp'].dt.date
    df['match_date'] = df['match_timestamp'].dt.date

    # Calculate cumulative counts
    likes_per_day = df.groupby('like_date').size().cumsum()
    matches_per_day = df.groupby('match_date').size().cumsum()

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot likes and matches on the same graph
    likes_per_day.plot(kind='line', ax=ax, label='Likes', linestyle='-', color='blue')
    matches_per_day.plot(kind='line', ax=ax, label='Matches', linestyle='-', color='green')

    # Add title, labels, legend, and format x-axis
    ax.set_title('Likes and Matches Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Count')
    ax.legend(loc='upper left')  # Place the legend on the top-left
    ax.tick_params(axis='x', rotation=45)

    # Display the plot in Streamlit
    st.pyplot(fig)

def plot_matches_by_time(df):
    # Ensure the timestamp is in datetime format
    df['match_timestamp'] = pd.to_datetime(df['match_timestamp'])
    # Extract the hour
    df['hour'] = df['match_timestamp'].dt.hour

    # Count matches by hour
    hour_match_counts = df.groupby('hour').size()

    time_labels = [
        "12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM",
        "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM",
        "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"
    ]

    # Plot matches by hour
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=hour_match_counts.index, y=hour_match_counts.values, ax=ax)

    ax.set_xticks(range(24))
    ax.set_xticklabels(time_labels, rotation=90)

    ax.set_title('Matches by Time of Day')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Number of Matches')
    st.pyplot(fig)

def plot_voice_notes_sent(df):
    if 'num_voice_notes' in df.columns:
        # Filter data for entries where num_voice_notes > 0
        voice_notes = df[df['num_voice_notes'] > 0]

        # Calculate value counts for the bar plot
        value_counts = voice_notes['num_voice_notes'].value_counts().sort_index()

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax)
        ax.set_title('Number of Voice Notes Sent')
        ax.set_xlabel('Number of Voice Notes')
        ax.set_ylabel('Frequency')

        # Display the plot in Streamlit
        st.pyplot(fig)

def plot_sankey(df):
    make_sankey(df, ["like_type", "match_type"])