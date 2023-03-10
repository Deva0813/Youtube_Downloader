from pytube import YouTube 
import os,sys
import re


def progressive_streams(): #progressive streams
    print("Enter the resolution you want to download(i.e. 1,2,3..): ")
    streams=[]
    for i in s.filter(progressive=True):
        res={}
        res["res"]=[i.resolution]
        res["itag"]=[i.itag]    
        streams.append(res)
        print(str((len(streams)))+". "+i.resolution)
    choice=int(input("\nEnter your choice: "))
    print("Downloading...")
    #download the video in Downloads folder
    vid = s.get_by_itag(streams[choice-1]["itag"][0]).download("Downloads",filename_prefix=streams[choice-1]["res"][0]+"_")
    if vid:
        print("Downloaded successfully , Check your Downloads folder... "+"Downloads")
    else:
        print("Download failed")
    
def non_progressive_streams(): #non progressive streams
    print("Enter the resolution you want to download(i.e. 1,2,3..): ")
    streams={}
    video=[]
    audio=[]
    print("\nVideo Formats: ")
    for i in s.filter(only_video=True,mime_type="video/mp4"):
        res={}
        if re.findall("^av01", i.video_codec):
            res["video_codec"]=[i.video_codec]
            res["res"]=[i.resolution]
            res["itag"]=[i.itag]
            res["size"]=[i.filesize]
            video.append(res)
            print(str((len(video)))+". "+i.resolution+" - "+f"{((i.filesize)/1024/1024):.2f}"+" MB")
    streams["Video"]=video
    video_choice=int(input("\nEnter your choice for video: "))
    print("\nAudio Formats:")
    for i in s.filter(only_audio=True,mime_type="audio/mp4"):
        aud={}
        aud["audio_codec"]=[i.audio_codec]
        aud["res"]=[i.abr]
        aud["itag"]=[i.itag]
        aud["size"]=[i.filesize]
        audio.append(aud)
        print(str((len(audio)))+". "+i.abr+" - "+f"{((i.filesize)/1024/1024):.2f}"+" MB")
    streams["Audio"]=audio
    audio_choice=int(input("\nEnter your choice for audio: "))
    
    print("Downloading...")
    #download the video in current folder
    vid_chk = s.get_by_itag(streams["Video"][video_choice-1]["itag"][0]).download("./Downloads/Merge/video",filename="video.mp4")
    aud_chk = s.get_by_itag(streams["Audio"][audio_choice-1]["itag"][0]).download("./Downloads/Merge/audio",filename="audio.mp4")
    
    if vid_chk and aud_chk:
        print("Downloaded successfully , Check your folder... ")

def merger():
    #print current directory
    title = re.sub(r'[^\w\s]', '', yt.title)
    title = title.replace(" ","_")
    run = "cd ./ffmpeg/bin/ && ffmpeg.exe -i ../../Downloads/Merge/video/video.mp4 -i ../../Downloads/Merge/audio/audio.mp4 -c:v copy -c:a aac -strict experimental ../../Downloads/"+title+".mp4"
    os.system(run)
    print("Merged successfully , Check your folder... ")
    

isActive=True
url = input("Enter the URL: ")


while isActive:
    yt = YouTube(url)
    s=yt.streams    
    
    print("\n---------------------------------INFO---------------------------------")
    print("Title: "+yt.title)
    print("Views: "+str(yt.views))
    print("Length: "+str(yt.length)+" seconds")
    print("Rating: "+str(yt.rating))
    print("Thumbnail: "+yt.thumbnail_url)
    print( "----------------------------------------------------------------------\n")
    
    
    print("Enter the type of stream you want to download: ")
    print("1. Progressive Streams")
    print("2. Non-Progressive Streams")
    print("3. Change URL")
    
    method = int(input("\nEnter your choice: "))
    
    if method==1:
        progressive_streams()
    elif method==2:
        non_progressive_streams()
        merger()
    elif method==3:
        url=input("\nEnter the URL: ")
    else:
        print("Invalid choice")
    
    print("\nDo you want to continue? (y/n)")
    if input()=='n':
        isActive=False
        sys.exit()
