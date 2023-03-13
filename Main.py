from pytube import YouTube 
import os,sys

def progressive_streams(): #progressive streams
    global pass_req
    pass_req = True
    print("Enter the resolution you want to download(i.e. 1,2,3..): ")
    streams=[]
    for i in s.filter(progressive=True):
        res={}
        res["res"]=[i.resolution]
        res["itag"]=[i.itag]    
        streams.append(res)
        print(str((len(streams)))+". "+i.resolution)
    print("'q'- Go Back")
    try:
        choice=int(input("\nEnter your choice: "))
        print("Downloading...")
        resol = streams[choice-1]["res"][0]
        #download the video in Downloads folder
        vid = s.get_by_itag(streams[choice-1]["itag"][0]).download("./Downloads",filename_prefix=resol+"-")
        if vid:
            print("Downloaded successfully , Check your Downloads folder... "+"Downloads")
        else:
            print("Download failed")
    except:
        print("Invalid choice")
        pass_req = False
        pass
            
def non_progressive_streams(): #non progressive streams
    global pass_req
    pass_req = True
    print("Enter the resolution you want to download(i.e. 1,2,3..): ")
    streams={}
    video=[]
    audio=[]
    itag_video=None
    print("\nVideo Formats: ")
    for i in s.filter(only_video=True):
        res={}
        # if re.findall("^av01", i.video_codec):
        if True:
            res["video_codec"]=i.video_codec
            res["res"]=i.resolution
            res["itag"]=i.itag
            res["size"]=i.filesize
            res["mime_type"]=i.mime_type
            video.append(res)
            #print(str((len(video)))+". "+i.resolution+" - "+f"{((i.filesize)/1024/1024):.2f}"+" MB"+" - "+i.mime_type)
    streams["Video"]=video
    res=[]
    for i in streams["Video"]:
        res.append(i["res"])
    res = set(res)
    so = sorted(res, key=lambda x: int(x.split("p")[0]))
    for i in range(len(so)):
        print(str(i+1)+". "+so[i])
    
    reso = int(input("\nEnter the resolution you want to download: "))
    format =[]
    for i in streams["Video"]:
        if so[reso-1] ==i["res"]:
            format.append(i)
    
    mimetype=list(set([i["mime_type"] for i in format]))
    print("\nMime Types(Video): ")
    for i in range(len(mimetype)):
        print(str(i+1)+". "+mimetype[i])
    
    mime = int(input("\nEnter the format you want to download: "))
    video_codec=[]
    for i in format:
        if mimetype[mime-1] ==i["mime_type"]:
            video_codec.append(i)
    
    video_code = list(set([i["video_codec"] for i in video_codec]))
    print("\nVideo Codecs: ")
    for i in range(len(video_code)):
        print(str(i+1)+". "+video_code[i])
    
    video_c = int(input("\nEnter the video codec you want to download: "))
    for i in video_codec:
        if video_codec[video_c-1]["video_codec"] ==i["video_codec"]:
            print("Downloading...")
            itag_video = i.get("itag")
            
    print("\nAudio Formats:")
    for i in s.filter(only_audio=True):
        aud={}
        aud["audio_codec"]=i.audio_codec
        aud["res"]=i.abr
        aud["itag"]=i.itag
        aud["size"]=i.filesize
        audio.append(aud)
        print(str((len(audio)))+". "+i.abr+" - "+f"{((i.filesize)/1024/1024):.2f}"+" MB")
    streams["Audio"]=audio
    audio_choice=int(input("\nEnter your choice for audio: "))
    
    print("\n---------------------------- Download Info: ----------------------------")
    print("Title: "+yt.title)
    print("Resolution: "+s.get_by_itag(itag_video).resolution)
    print("Video Codec: "+s.get_by_itag(itag_video).video_codec)
    print("Mime Type: "+s.get_by_itag(itag_video).mime_type)
    print("Audio Codec: "+s.get_by_itag(streams["Audio"][audio_choice-1]["itag"]).audio_codec)
    print("Audio Bitrate: "+s.get_by_itag(streams["Audio"][audio_choice-1]["itag"]).abr)
    print("Size: Video - "+f"{((s.get_by_itag(itag_video).filesize)/1024/1024):.2f}"+" MB "+"Audio - "+f"{((s.get_by_itag(streams['Audio'][audio_choice-1]['itag']).filesize)/1024/1024):.2f}"+" MB")
    
    print("-----------------------------------------------------------------------")
    
    cont = input("Do you want to continue? (y/n): ")
    if cont.lower() == "y":
        print("Downloading...")
        #download the video in current folder
        vid_chk = s.get_by_itag(itag_video).download("./Downloads/Merge/video",filename_prefix="video-")
        aud_chk = s.get_by_itag(streams["Audio"][audio_choice-1]["itag"]).download("./Downloads/Merge/audio",filename_prefix="audio-")
        
        if vid_chk and aud_chk:
            print("Downloaded successfully , Check your folder... ")
        merger()   
    else:
        pass_req = False
        pass
    
def only_audio(): #only audio
    audio=[]
    print("\nAudio Formats:")
    for i in s.filter(only_audio=True):
        aud={}
        aud["audio_codec"]=i.audio_codec
        aud["res"]=i.abr
        aud["itag"]=i.itag
        aud["size"]=i.filesize
        audio.append(aud)
        print(str((len(audio)))+". "+i.abr+" - "+f"{((i.filesize)/1024/1024):.2f}"+" MB")
    audio_choice=int(input("\nEnter your choice for audio: "))
    print("\n---------------------------- Download Info: ----------------------------")
    print("Title: "+yt.title)
    print("Audio Codec: "+s.get_by_itag(audio[audio_choice-1]["itag"]).audio_codec)
    print("Audio Bitrate: "+s.get_by_itag(audio[audio_choice-1]["itag"]).abr)
    print("Size: "+f"{((s.get_by_itag(audio[audio_choice-1]['itag']).filesize)/1024/1024):.2f}"+" MB")
    print("-----------------------------------------------------------------------")
    choice = input("Do you want to continue? (y/n): ")
    if choice.lower() == "y":
        print("Downloading...")
        #download the video in current folder
        aud_chk = s.get_by_itag(audio[audio_choice-1]["itag"]).download("./Downloads/",filename_prefix="audio-")
        if aud_chk:
            print("Downloaded successfully , Check your folder... ")
        

def merger():
    #print current directory
    title = yt.title
    title = title.replace(" ","_").replace("|","-")
    title = "../../Downloads/"+title+".mp4"
    video = select_file("./Downloads/Merge/video","video-")
    video = "../../Downloads/Merge/video/"+video
    audio = select_file("./Downloads/Merge/audio","audio-")
    audio = "../../Downloads/Merge/audio/"+audio
    print(video)
    print(audio)
    run = f'cd ./ffmpeg/bin/ && ffmpeg.exe -i "{video}" -i "{audio}" -c:v copy -c:a aac -strict experimental "{title}"'
    print(run)
    os.system(run)
    print("Merged successfully , Check your folder... ")
    remove_files()

#remove the temp files    
def remove_files():
    print("Removing temp files...")
    os.remove("./Downloads/Merge/video/"+select_file("./Downloads/Merge/video","video-"))
    os.remove("./Downloads/Merge/audio/"+select_file("./Downloads/Merge/audio","audio-"))
    os.rmdir("./Downloads/Merge/video")
    os.rmdir("./Downloads/Merge/audio")
    os.rmdir("./Downloads/Merge")
    print("Removed successfully ")
    
#select the file with the start name in the folder
def select_file(f_path,f_name):
    for file in os.listdir(f_path):
        if file.startswith(f_name):
            return file
    return None

# #-----------------------------------------------------------------UNZIP----------------------------------------------------------------
# with zipfile.ZipFile("./ffmpeg.zip", 'r') as zip_ref:
#     zip_ref.extractall("./ffmpeg")
#-----------------------------------------------------------------MAIN-----------------------------------------------------------------   
os.system("cls")

print('''\n░█░█░█▀█░█░█░▀█▀░█░█░█▀▄░█▀▀░░░█▀▄░█▀█░█░█░█▀█░█░░░█▀█░█▀█░█▀▄░█▀▀░█▀▄
░░█░░█░█░█░█░░█░░█░█░█▀▄░█▀▀░░░█░█░█░█░█▄█░█░█░█░░░█░█░█▀█░█░█░█▀▀░█▀▄
░░▀░░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀░░▀▀▀░░░▀▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀''')    
print("\n------------------------ Creator : Devanand.M ------------------------")
print("------------------------ Version : 1.0 -------------------------------")
print("------------------------ Date : 13/03/2023 ---------------------------")
print("--------------------- https://github.com/Deva0813 --------------------")

isActive=True
url = ""
pass_req=True

url = input("\nEnter the URL: ")
while isActive:
    os.system("cls")
    yt = YouTube(url)
    s=yt.streams    
    
    print('''\n░█░█░█▀█░█░█░▀█▀░█░█░█▀▄░█▀▀░░░█▀▄░█▀█░█░█░█▀█░█░░░█▀█░█▀█░█▀▄░█▀▀░█▀▄
░░█░░█░█░█░█░░█░░█░█░█▀▄░█▀▀░░░█░█░█░█░█▄█░█░█░█░░░█░█░█▀█░█░█░█▀▀░█▀▄
░░▀░░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀░░▀▀▀░░░▀▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀''')
    print("\n------------------------ Creator : Devanand.M ------------------------")
    print("------------------------ Version : 1.0 -------------------------------")
    print("------------------------ Date : 13/03/2023 ---------------------------")
    print("--------------------- https://github.com/Deva0813 --------------------")
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
    print("4. Only Audio")
    print("5. Exit")
    
    method=(input("\nEnter your choice: "))
    
    if method.isdigit():
        method=int(method)
    else:
        print("Invalid choice")
    
    if method==1:
        progressive_streams()
    elif method==2:
        non_progressive_streams()
    elif method==3:
        url=input("\nEnter the URL: ")
    elif method==4:
        only_audio()
    elif method==5:
        isActive=False
        sys.exit()
    else:
        print("Invalid choice")
    
    if pass_req:
        print("\nDo you want to continue? (y/n)")
        if input()=='n':
            isActive=False
            sys.exit()

    pass_req=True   
