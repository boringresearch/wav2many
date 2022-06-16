
import glob
import os
import string
import datetime
import streamlit as st
import subprocess
import glob
import librosa
from pydub import AudioSegment
import math
import shutil

class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '/' + filename
        
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + '/' + split_filename, format="wav")
        
    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')

uploaded_file = st.sidebar.file_uploader(label = "Please upload your file ",
type=['wav', 'mp3'])
length_audio = librosa.get_duration(filename=uploaded_file.name)/60

# convert to wav
format_ = uploaded_file.name.split('.')[-1]
outputname = uploaded_file.name + ".wav"
sound = AudioSegment.from_file(uploaded_file.name, format= format_)
sound.export(outputname, format="wav")

values = st.sidebar.slider(
     'Number of Mins',
     0, 30, 1)

submit_button = st.sidebar.button(label='Submit')


st.title("Audio2Many")
st.write('一共有', round(length_audio, 2) , "分钟")
st.write('被分成', math.ceil(round(length_audio, 2)/values) , "份")


# Main app engine
if __name__ == "__main__":
    # display title and description
    
    folder = "./"
    
    if submit_button:

      # # remove files
      # files = glob.glob('./*.wav')
      # for f in files:
      #     try:
      #         f.unlink()
      #     except OSError as e:
      #         print("Error: %s : %s" % (f, e.strerror))
      # genrate data
      split_wav = SplitWavAudioMubin(folder, uploaded_file.name + ".wav")
      split_wav.multiple_split(min_per_split=values)

      # downloadable button
      shutil.make_archive("小碎片们.zip", 'zip', "./")

      with open("小碎片们.zip", 'rb') as f:
        st.download_button('Download File', f, file_name="小碎片们.zip")  # Defaults to 'application/octet-stream'
