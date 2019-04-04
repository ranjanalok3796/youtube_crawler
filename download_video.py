from pytube import YouTube
import os
from os import path
import sys
# print(len(all_streams)

def filter_stream( yt ):
    # prog_streams = yt.streams.all()
    # print(prog_streams)
    print("filter Videos")
    ytube = yt
    prog_streams = ytube.streams.filter(progressive=True).all()
    for stream in prog_streams:
        # print(stream, end=" ")
        filesize = stream.filesize
        # print(filesize)
        if filesize < 61440000:
            mystream = stream
            break
    return mystream

def filter_stream_audio( yt ):
    # prog_streams = yt.streams.all()
    atube = yt
    print("Filter out Audio files")
    audio_streams = atube.streams.filter(only_audio=True).all()
    mystream = audio_streams[len(audio_streams)-1]
    for stream in audio_streams:
        # print(stream, end=" ")
        filesize = stream.filesize
        # print( str(filesize))
        if filesize < 5120000 and filesize > mystream.filesize:
            mystream = stream
    # print(mystream,end=" ")
    # print(str(mystream.filesize))
    return mystream


# def progress_func(self,stream, chunk,file_handle, bytes_remaining):
#     size = video.filesize
#     p = 0
#     while p <= 100:
#         progress = p
#         print (str(p)+'%')
#         p = percent(bytes_remaining, size)
#
# def percent(self, tem, total):
#         perc = (float(tem) / float(total)) * float(100)
#         return perc

def download_video( link, folder ):
    video_folder = "../Crawler-Output/Videos/"+folder
    audio_folder = "../Crawler-Output/Audios/"+folder
    try:
        os.mkdir(video_folder)
        print("Directory " , video_folder ,  " Created ")
    except FileExistsError:
        print("Directory " , video_folder ,  " already exists")

    try:
        os.mkdir(audio_folder)
        print("Directory " , audio_folder ,  " Created ")
    except FileExistsError:
        print("Directory " , audio_folder ,  " already exists")

    yt = YouTube(link)
    video_title = yt.title
    # print(video_title)
    video_stream = filter_stream(yt)
    audio_stream = filter_stream_audio(yt)
    # print(video_stream)
    # print(audio_stream)
    video_filename = video_stream.default_filename
    audio_filename = audio_stream.default_filename
    # print(video_filename)
    # print(audio_filename)
    video_file_path = video_folder+"/"+video_filename
    audio_file_path = audio_folder+"/"+video_title+".mp3"
    # print(video_file_path)
    # print(audio_file_path)

    if path.exists(video_file_path):
        print("Video Already Exists = "+video_file_path)
    else:
        print("Downloading Video = "+ str(video_filename))
        video_stream.download(video_folder)

    # print ("Creating Audio = "+str(audio_filename))
    if path.exists(audio_file_path):
        print("Audio Already Exists = "+audio_file_path)
    else:
        print("Creating Audio = "+ str(audio_filename))
        command = "ffmpeg -i \'"+video_file_path+"\' -ab 160k -ac 2 -ar 44100 \'"+audio_file_path+"'"
        # audio_stream.download(audio_folder)
        os.system(command)
