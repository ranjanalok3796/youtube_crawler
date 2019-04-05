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

def upload_bucket( video_path, audio_path ):
    video_upload_command = "gsutil cp '"+video_path+"' 'gs://videos-dbst-shutapp/"+video_path+"'"
    os.system(video_upload_command)
    remove_video_command = "rm '"+video_path+"'"
    os.system(remove_video_command)
    print("Video Removed")
    audio_upload_command = "gsutil cp '"+audio_path+"' 'gs://videos-dbst-shutapp/"+audio_path+"'"
    os.system(audio_upload_command)
    remove_audio_command = "rm '"+audio_path+"'"
    os.system(remove_audio_command)
    print("Audio Removed")

def correction ( name ):
    name = name.replace(" ","_")
    name = name.replace("[","_")
    name = name.replace("]","_")
    name = name.replace("(","_")
    name = name.replace(")","_")
    name = name.replace("{","_")
    name = name.replace("}","_")
    return name

def download_video( link, folder ):
    folder = correction(folder)
    video_folder = "Videos/"+folder
    audio_folder = "Audios/"+folder
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
    # audio_stream = filter_stream_audio(yt)
    # print(video_stream)
    # print(audio_stream)
    # video_filename = video_stream.default_filename
    video_filename = correction(video_title)
    audio_filename = correction(video_title)
    print("Video = "+video_filename)
    # print(audio_filename)
    video_file_path = video_folder+"/"+video_stream.default_filename
    video_file_path = correction(video_file_path)
    audio_file_path = audio_folder+"/"+audio_filename+".mp3"
    audio_file_path = correction(audio_file_path)
    print("Video Path = "+video_file_path)
    print("Audio Path = "+audio_file_path)

    if path.exists(video_file_path):
        print("Video Already Exists = "+video_file_path)
    else:
        print("Downloading Video = "+ str(video_filename))
        video_stream.download(video_folder, video_filename)

    # print ("Creating Audio = "+str(audio_filename))
    if path.exists(audio_file_path):
        print("Audio Already Exists = "+audio_file_path)
    else:
        print("Creating Audio = "+ str(audio_filename))
        command = "ffmpeg -i \'"+video_file_path+"\' -ab 160k -ac 2 -ar 44100 \'"+audio_file_path+"'"
        # audio_stream.download(audio_folder)
        os.system(command)

    if path.exists(video_file_path):
        upload_bucket(video_file_path,audio_file_path)
    else:
        print("Could not run upload bucket command")
