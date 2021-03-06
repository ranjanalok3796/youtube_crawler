from pytube import YouTube
import os
from os import path
import sys
import subprocess
import logging
import time
import datetime

current_date = datetime.datetime.now()
if ( current_date.hour < 6 ):
     log_file_name = 'logs/'+str(current_date.date())+'_1.log'
elif ( current_date.hour < 12 and current_date.hour > 6 ) :
    log_file_name = 'logs/'+str(current_date.date())+'_2.log'
elif ( current_date.hour < 18 and current_date.hour > 12 ) :
    log_file_name = 'logs/'+str(current_date.date())+'_3.log'
else :
    log_file_name = 'logs/'+str(current_date.date())+'_4.log'

logging.basicConfig(filename=log_file_name,level=logging.INFO)

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
    video_upload_command = "gsutil cp \""+video_path+"\" \"gs://videos-dbst-shutapp/"+video_path+"\""
    returned_value = subprocess.check_output(video_upload_command, shell=True)  # returns the exit code in unix
    # os.system(video_upload_command)
    logging.info(str(time.asctime( time.localtime(time.time()) )) + str(returned_value.decode("utf-8")))
    remove_video_command = "rm '"+video_path+"'"
    os.system(remove_video_command)
    logging.info(str(time.asctime( time.localtime(time.time()) )) +" Video Removed from Local Instance")
    # print("Video Removed")

    audio_upload_command = "gsutil cp \""+audio_path+"\" \"gs://videos-dbst-shutapp/"+audio_path+"\""
    returned_value = subprocess.check_output(audio_upload_command, shell=True)  # returns the exit code in unix
    # os.system(audio_upload_command)
    logging.info(str(time.asctime( time.localtime(time.time()) )) + str(returned_value.decode("utf-8")))
    logging.info(str(time.asctime( time.localtime(time.time()) )) +" Audio Copied to Google Bucket")
    remove_audio_command = "rm '"+audio_path+"'"
    os.system(remove_audio_command)
    logging.info(str(time.asctime( time.localtime(time.time()) )) +" Audio Removed from local Instance")
    # print("Audio Removed")

def correction ( name ):
    name = name.replace(" ","_")
    name = name.replace("[","_")
    name = name.replace("]","_")
    name = name.replace("(","_")
    name = name.replace(")","_")
    name = name.replace("{","_")
    name = name.replace("}","_")
    name = name.replace("\'","_")
    name = name.replace("\"","_")
    return name

def download_video( link, folder ):
    folder = correction(folder)
    video_folder = "Videos/"+folder
    audio_folder = "Audios/"+folder
    # os.mkdir(video_folder)
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
    # print("Video Path = "+video_file_path)
    # print("Audio Path = "+audio_file_path)

    if path.exists(video_file_path):
        print("Video Already Exists = "+video_file_path)
        logging.info( str(time.asctime( time.localtime(time.time()) )) +"Video Already Exists = "+video_filename)
    else:
        print("Downloading Video = "+ str(video_filename))
        video_stream.download(video_folder, video_filename)
        logging.info(str(time.asctime( time.localtime(time.time()) )) +"File Downloaded = "+video_filename)

    # print ("Creating Audio = "+str(audio_filename))
    if path.exists(audio_file_path):
        print("Audio Already Exists = "+audio_file_path)
        logging.info( str(time.asctime( time.localtime(time.time()) )) +"Audio Already Exists = "+audio_filename)
    else:
        print("Creating Audio = "+ str(audio_filename))
        command = "ffmpeg -i \'"+video_file_path+"\' -ab 160k -ac 2 -ar 44100 \'"+audio_file_path+"'"
        # audio_stream.download(audio_folder)
        os.system(command)
        logging.info(str(time.asctime( time.localtime(time.time()) )) +"Audio Created = "+audio_filename)

    if path.exists(video_file_path):
        upload_bucket(video_file_path,audio_file_path)
    else:
        print("Could not run upload bucket command")
