import pandas as pd
import plotly.express as px
from pywebio.output import *
from pywebio.input import *
from pywebio.session import *
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
import random
from pywebio.output import put_markdown
from pywebio.input import input_group, input, TEXT
from pywebio.output import put_text

def discussion_dashboard(transcript_data):
    clear()
    put_image("https://github.com/NorikaNarimatsu/Multimedia_final/blob/main/logo.png?raw=true", width='250px').style(
        'display: block; margin-left: auto; margin-right: auto;')


    # Collect user inputs for speakers and keywords in a single input_group
    user_inputs = input_group(
        "In your audio file, we identify 3 speakers. Enter Speaker Names and Keywords",
        [
            input("Enter the name for Speaker 0:", name="speaker_0", type=TEXT),
            input("Enter the name for Speaker 1:", name="speaker_1", type=TEXT),
            input("Enter the name for Speaker 2:", name="speaker_2", type=TEXT),
            input("Enter keywords (comma-separated):", name="keywords", type=TEXT),
        ],
    )

    # Access the user inputs
    speaker_0 = user_inputs["speaker_0"]
    speaker_1 = user_inputs["speaker_1"]
    speaker_2 = user_inputs["speaker_2"]
    keywords_input = user_inputs["keywords"]

    # Create a DataFrame from the transcript data
    df = pd.DataFrame(transcript_data)

    # Convert timestamp to datetime for better plotting
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%M:%S.%f')

    # Convert the timestamp to string for animation
    df['timestamp_str'] = df['timestamp'].dt.strftime('%M:%S.%f')

    # Define the mapping of original speaker names to new names
    speaker_mapping = {'SPEAKER_00:': speaker_0, 'SPEAKER_01:': speaker_1, 'SPEAKER_02:': speaker_2}

    # Replace speaker names using the map function
    df['speaker'] = df['speaker'].map(speaker_mapping)

    # Group by speaker and timestamp and concatenate the text
    full_text_df = df.groupby(['speaker', 'timestamp'])['text'].apply(lambda x: ' '.join(x)).reset_index()

    # Concatenate all text from different speakers and timestamps
    full_text = ' '.join(full_text_df['text'])

    # Calculate the cumulative word count for each speaker
    speaker_word_counts = df.groupby('speaker')['word_count'].sum()

    # Calculate the ratio of word count for each speaker
    speaker_word_ratios = speaker_word_counts / speaker_word_counts.sum()

    # Report speaker word counts and ratios
    put_markdown("## Speaker Word Counts and Ratios:")
    for speaker, word_count, ratio in zip(speaker_word_ratios.index, speaker_word_counts, speaker_word_ratios):
        put_text(f"- {speaker}: Word Count = {word_count}, Ratio = {ratio:.2%}")

    # Create an animated bar plot with Plotly Express
    fig = px.bar(df, x='speaker', y='cumulative_word_count', color='speaker',
                animation_frame='timestamp_str',
                title='Cumulative Word Count Over Time for Each Speaker',
                labels={'timestamp_str': 'Timestamp', 'cumulative_word_count': 'Cumulative Word Count'},
                category_orders={'speaker': sorted(df['speaker'].unique())},
                )

    # Update layout for better readability
    fig.update_layout(xaxis=dict(title='Speaker'),
                    yaxis=dict(title='Cumulative Word Count', range=[0, 500]),
                    )

    # Convert Plotly figure to HTML
    fig_html = fig.to_html(include_plotlyjs="require", full_html=False)
    put_markdown("## Group Discussion Dynamics:")
    # Show the Plotly figure as HTML for cumulative word count
    put_html(fig_html)

    keywords = [kw.strip() for kw in keywords_input.split(',')]

    # Initialize a dictionary to store keyword counts
    keyword_counts = {kw: full_text.lower().count(kw.lower()) for kw in keywords}

    # Report keyword counts
    put_markdown("## Keyword Counts:")
    for keyword, count in keyword_counts.items():
        put_text(f"- {keyword}: {count} occurrences")

    # Highlight keywords in the full text with color
    highlighted_text = full_text
    for keyword in keywords:
        # Use a unique color for each keyword
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        highlighted_text = highlighted_text.replace(keyword, f'<span style="background-color: {color}; padding: 2px; border-radius: 4px;">{keyword}</span>')

    # Show the highlighted text on the dashboard as HTML
    put_html(f"<div style='font-size: 14px;'>{highlighted_text}</div>")

    # Download NLTK punkt if not already downloaded
    nltk.download('punkt')

    # Use the full_text variable for summarization
    text_to_summarize = full_text

    # Choose the language and create a parser
    language = "english"
    parser = PlaintextParser.from_string(text_to_summarize, Tokenizer(language))

    # Create an LSA (Latent Semantic Analysis) summarizer
    lsa_summarizer = LsaSummarizer()

    # Summarize the text
    summary = lsa_summarizer(parser.document, sentences_count=8)  # You can adjust the number of sentences in the summary

    # Display the summarized text using PyWebIO
    put_markdown(f"## Summarized Text\n{' '.join(str(sentence) for sentence in summary)}")
