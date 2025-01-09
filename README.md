# Hinge Data Analyzer

An app that given a users hinge match data, shows visualizations about the information provided.
Visualizations include:

Sankey of like types to if they got a match (like sent and recieved to matched or not matched)

Line graph of matches over time

Histplot of time between like and match

Histplot of time between first and last message (length of conversation)

Histplot of average time between messages

Histplot of distribution of number of messages in a conversation

Scatterplot with correlation between number of messages in a conversation and average time between messages


Other additional statistics are provided including:

Average messages per match, likes per day (sent and received), matches per day, like to match percentages for both likes sent and receieved and the aggregate of those, total messages sent, total matches met, and total voice notes sent.

Streamlit was used to create the app and the visualizations were made with seaborn, matplotlib, and plotly.

FILES:
-----
app:

static/hlogo: logo for homepage and tab

Home: contains all streamlit functions to make the homepage, calls visualizations to show, and loads the hinge matches jsonand calls the data reader to convert it into a pandas dataframe for the visualizations. 

__init__: initializes app folder


code:

__init__: intializes code folder

data_reader: given the hinge matches json; reads, converts, and returns a data frame of all used information

sankey: creates the sankey graph of likes to matches

viz: creates all visualizations including the sankey for simplied importing


.streamlit: streamlit specifications


HOW TO USE
----------

Download all files and imports, and in a terminal within the directory run the following:
streamlit run app/Home.py      (add python -m to the beginning if this does not work)

