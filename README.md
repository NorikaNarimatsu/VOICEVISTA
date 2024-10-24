# Speech Recognition and Analysis for Group Discussion

## Description:
This is the code of the project Speech Recognition and Analysis for Group Discussions written by Norika Narimatsu and Xiaolin Gu.

## Installation:
Requirements:
* `python3`
* `pyannote-audio`
* `plotly.express`
* `numpy`
* `pywebio`
* `matplotlib`
* `seaborn`
* `typing`
* `pandas`
* `sumy`
* `whisper-timestamped`

Another way to install `whisper-timestamped`:
```bash
git clone https://github.com/linto-ai/whisper-timestamped
cd whisper-timestamped/
python3 setup.py install
```

## Usage:
Install all packages required above first.
Then run 'python3 app.py', it will return you a link in the terminal.
Go to the link, and you can upload the audio file to the website. Remember it only accepts .wav file.
The system will start analyzing immediately but it will take some time. You can see the analyzation process in your terminal.
After analyzation, click the 'Dashboard' buttom. The system can detect how many people are involved in the discussion. You can input the name of the speakers and the keywords you want to detect.
The result will show on your Dashboard, including the speaking proportion of each speaker, the whole contents with keywords highlighted and a summarized text. You can change the timeline to see how the proportion changes.