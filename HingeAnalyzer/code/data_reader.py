import pandas as pd
from datetime import datetime

def transform_data(json_data):
    """ Function to convert hinges matches json into a clean, easily usable dataframe
    Additionally created new columns of data such as average time between messages
    """
    rows = []
    
    for interaction in json_data:
        # Create a base row dictionary
        row = {}
        
        # Matches
        if 'match' in interaction:
            row['match_type'] = 'match'
            row['match_timestamp'] = interaction['match'][0]['timestamp']
        else:
            row['match_type'] = 'no_match'
            row['match_timestamp'] = None
        
        # Likes
        if 'like' in interaction:
            row['like_type'] = 'sent'
            row['like_timestamp'] = interaction['like'][0]['timestamp']
        else:
            row['like_type'] = 'recieved'
            row['like_timestamp'] = None
        
        # Blocks
        if 'block' in interaction:
            row['block_type'] = interaction['block'][0]['block_type']
            row['blocked_timestamp'] = interaction['block'][0]['timestamp']
        else:
            row['block_type'] = None
            row['blocked_timestamp'] = None

        # We met
        if 'we_met' in interaction:
            row['met'] = interaction['we_met'][0]['did_meet_subject']
        else:
            row['met'] = None
        # Chats
        if 'chats' in interaction:
            chats = interaction['chats']
            row['num_messages'] = len(chats)
            
            # Convert timestamps of messages to datetime, ensuring it's a string first
            timestamps = []
            for chat in chats:
                timestamp = chat['timestamp']
                if isinstance(timestamp, str):
                    # If it's a string, parse it to datetime
                    timestamps.append(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
                elif isinstance(timestamp, datetime):
                    # If it's already a datetime object, just append it
                    timestamps.append(timestamp)
            
            # Sort timestamps chronologically
            timestamps.sort()
            
            # Calculate the time between the first and last message
            if len(timestamps) > 1:
                first_last_time_diff = (timestamps[-1] - timestamps[0]).total_seconds()
            else:
                first_last_time_diff = None
            
            row['time_between_first_and_last_message'] = first_last_time_diff
            
            # Calculate the average time between messages
            if len(timestamps) > 1:
                time_differences = [(timestamps[i] - timestamps[i-1]).total_seconds() for i in range(1, len(timestamps))]
                avg_time_between_messages = sum(time_differences) / len(time_differences)
            else:
                avg_time_between_messages = None  # No time difference if only one message
            
            row['avg_time_between_messages'] = avg_time_between_messages
            
            # Calculate the average message length (in words), but handle missing body
            message_lengths = [len(chat['body'].split()) if 'body' in chat else 0 for chat in chats]
            avg_message_length = sum(message_lengths) / len(message_lengths) if message_lengths else 0
            
            row['avg_message_length'] = avg_message_length
        else:
            row['num_messages'] = 0
            row['avg_time_between_messages'] = None
            row['avg_message_length'] = 0
            row['time_between_first_and_last_message'] = None

        # Calculate the time between match and first message 
        if 'match_timestamp' in row and row['match_timestamp'] is not None:
            match_timestamp = row['match_timestamp']
            if isinstance(match_timestamp, str):
                match_timestamp = datetime.strptime(match_timestamp, "%Y-%m-%d %H:%M:%S")
            first_message_timestamp = timestamps[0]
            row['time_between_match_and_first_message'] = (match_timestamp - first_message_timestamp).total_seconds()
        else:
            row['time_between_match_and_first_message'] = None
        
        # Calculate the time between like sent and match (if 'like' and 'match' exist)
        if 'like_timestamp' in row and row['like_timestamp'] is not None and row['match_timestamp'] is not None:
            like_timestamp = row['like_timestamp']
            if isinstance(like_timestamp, str):
                like_timestamp = datetime.strptime(like_timestamp, "%Y-%m-%d %H:%M:%S")
            match_timestamp = row['match_timestamp']
            if isinstance(match_timestamp, str):
                match_timestamp = datetime.strptime(match_timestamp, "%Y-%m-%d %H:%M:%S")
            row['time_between_like_and_match'] = (match_timestamp - like_timestamp).total_seconds()
        else:
            row['time_between_like_and_match'] = None
        
        # Handle the 'voice_notes' key and count the number of voice notes
        if 'voice_notes' in interaction:
            row['num_voice_notes'] = len(interaction['voice_notes'])
        else:
            row['num_voice_notes'] = 0
        
        # Append the row to the rows list
        rows.append(row)
    
    # Convert the rows to a dataframe before returning
    df = pd.DataFrame(rows)
    return df
