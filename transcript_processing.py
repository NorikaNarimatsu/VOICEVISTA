import pandas as pd

def process_transcript_file(texts):
    with open(texts, 'r') as file:
        lines = file.readlines()

    # Create a list to store the timestamp, speaker, text, and word count information
    transcript = []

    # Get a list of all unique speakers
    all_speakers = set()

    # Iterate through the lines in the file and extract information
    for line in lines:
        # Assuming the speaker information is in a specific format, adapt as needed
        if line.startswith("[") and "]" in line:
            speaker = line.split(" ")[1]
            all_speakers.add(speaker)

    # Create initial dataframe with all speakers and zero cumulative word count
    initial_data = [{'timestamp': '', 'speaker': speaker, 'cumulative_word_count': 0} for speaker in all_speakers]
    df_initial = pd.DataFrame(initial_data)

    # Initialize variables for tracking word count over time for each speaker
    current_word_counts = {speaker: 0 for speaker in all_speakers}

    # Iterate through the lines in the file and extract information
    for line in lines:
        # A specific format, adapt as needed
        if line.startswith("[") and "]" in line:
            timestamp = line.split("]")[0][1:]
            text = " ".join(line.split(" ")[2:]).strip()

            # Calculate word count
            word_count = len(text.split())

            # Update word count for each speaker
            for speaker in all_speakers:
                # Check if the current speaker matches the loop speaker
                if speaker in line:
                    # Update cumulative word count for the current speaker
                    current_word_counts[speaker] += word_count

                    # Append information to the transcript list
                    transcript.append({
                        "timestamp": timestamp,
                        "speaker": speaker,
                        "text": text,
                        "word_count": word_count,
                        "cumulative_word_count": current_word_counts[speaker]
                    })
                else:
                    # If the speaker doesn't match, use zero word count
                    transcript.append({
                        "timestamp": timestamp,
                        "speaker": speaker,
                        "text": "",
                        "word_count": 0,
                        "cumulative_word_count": current_word_counts[speaker]
                    })
    return transcript
