import whisper_timestamped as whisper
from pyannote.audio import Pipeline


def asrWithTime(audio_file):
    '''
    do speech recognition and generate timestamp
    input: audio file
    output: two .vtt files
    '''
    audio = whisper.load_audio(audio_file)
    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(model, audio, language="en")
    txtWithTime = []
    for sen in result["segments"]:
        info = []
        info.append(sen["start"])
        info.append(sen["text"])
        txtWithTime.append(info)
    return txtWithTime

def secondsFormatted(seconds):
    '''
    adjust the format of timestamp
    input: 0.1 
    output: 00:00.100
    '''
    minutes, seconds = divmod(seconds, 60)
    seconds, milliseconds = divmod(seconds, 1)
    formatted = f"{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds * 1000):03d}"
    return formatted


def speakerDiarization(audio_file):
    '''
    do speaker diarization
    input: audio file
    output format: [0.008488964346349746, 0.05942275042444822, 'SPEAKER_02']
    '''
    pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.0",
    use_auth_token="hogehoge")
    diarization = pipeline(audio_file)

    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        result = [turn.start, turn.end, speaker]
        results.append(result)

    return results

def unifiedSpeaker(texts):
    '''
    the speakeer diarization is not compressing enough
    e.g. the time range speaker2 speaking may be divided to more than 1 records
    this function merges them into one record to facilitate subsequent processing
    '''
    newTexts = []
    speaker = texts[0][2]
    for i in range(len(texts)):
        if(texts[i][-1] != speaker):
            stop = texts[i-1][1]
            newTexts.append([stop, speaker])
            speaker = texts[i][-1]
        if(i == len(texts)-1):
            newTexts.append([texts[i][1], speaker])
            break
        if(texts[i][-1] == speaker):
            continue
    return newTexts

def combineSpeakerText(txtWithTime, txtWithSpeaker):
    '''
    combines speaker info and content info by timestamp
    '''
    speaker_time = txtWithSpeaker[0][0]
    speaker = txtWithSpeaker[0][1]
    speaker_row = 0
    full_info = []

    for line in txtWithTime:
        start_time = line[0]
        if(start_time>speaker_time):
            speaker_row += 1
            speaker_time = txtWithSpeaker[speaker_row][0]
            
        speaker = txtWithSpeaker[speaker_row][1]
        start_time = secondsFormatted(round(start_time, 1))
        full_info.append('['+str(start_time)+'] '+speaker+': '+line[1])

    return full_info
        
