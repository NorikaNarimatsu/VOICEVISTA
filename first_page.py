from pywebio.output import *
from pywebio.input import *
from pywebio.session import *
from pywebio.platform import *
from dashboard import discussion_dashboard 
from transcript_processing import process_transcript_file
from audio_processing import asrWithTime, speakerDiarization,  unifiedSpeaker, combineSpeakerText # Import the function from the other file

def first_page():
    clear()
    put_image("https://github.com/NorikaNarimatsu/Multimedia_final/blob/main/logo.png?raw=true", width='250px').style(
        'display: block; margin-left: auto; margin-right: auto;')
    put_markdown('# Welcome to VoiceVista').style(
        'text-align: center; margin: auto;  width: 80%; font-size: 40px')
    put_text(
        'In today’s world, effective communication is more crucial than ever, and VoiceVista aims to play an importan role in enhancing and facilitating group discussions. This project is motivated by the need to not only evaluate but also foster meaningful group discussion.')


    # Team members' contributions
    gu_contribution = "Speaker Recognition and Speaker Diarization using pyAudioAnalysis and hugging face's pipeline"
    norika_contribution = "Frontend using PywebIO and Plotly,Text Summalization and Keyword Detection"

    # Display team members and their contributions
    put_markdown('## Team Members:').style('text-align: center; margin: auto')
    put_text('- Gu Xiaolin: ' + gu_contribution)
    put_text('- Norika Narimatsu: ' + norika_contribution)
    put_text('- Leiden Institute of Advanced Computer Science (LIACS) / Multimedia System Course 2023 Fall Semester')

    # Add file upload and processing button
    audio_file = file_upload(label='Upload Audio File that You Would Like to Explore', accept='.wav', help_text='Upload a .wav audio file for processing')

    audio_file_upload = audio_file['filename']

    # Process audio and get the text
    #audio_file = "/Users/norika_machome/GitHub/Leiden/MultimediaSystem/final/speechProcess/audio8.wav"
    #texts = "/Users/norika_machome/GitHub/Leiden/MultimediaSystem/final/speechProcess/audio8.txt"

    txtWithTime = asrWithTime(audio_file_upload)
    txtWithSpeaker = speakerDiarization(audio_file_upload)
    txtWithSpeaker = unifiedSpeaker(txtWithSpeaker)
    texts = combineSpeakerText(txtWithTime, txtWithSpeaker)

    text_file = audio_file_upload[:-4] + ".txt"

    # write results to output file
    with open(text_file, "w", encoding="utf-8") as file:
        for text in texts:
            file.write(text+'\n')
    print(text_file)

    transcript_data = process_transcript_file(text_file)

    # Click Here for Dashboard button
    put_markdown('Upload is done! Click Here for the Dashboard').style('text-align: center;')
    put_buttons(['Dashboard'], onclick=[lambda: discussion_dashboard(transcript_data)]).style('text-align: center;')

if __name__ == '__main__':
    first_page()
    input()


