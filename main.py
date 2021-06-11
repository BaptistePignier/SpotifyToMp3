from bs4 import BeautifulSoup
import json
import requests
import youtube_dl
from youtubesearchpython import VideosSearch
import os

def time_conv(time):
	time = time.split(":")
	if len(time) == 1:
		return int(time[0])
	if len(time) == 2:
		return int(time[0]) * 60 + int(time[1])
	if len(time) == 3:
		return int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])

def condition(x,y):
	return (x > y - 60) & (x < y + 60)


print("Getting Spotify playlist ... ")

url = "https://open.spotify.com/playlist/4euMtNSFf0p2lFF2ivAEzb"
##url = "https://open.spotify.com/playlist/37i9dQZF1DZ06evO26xkaI"
page = requests.get(url).content.decode('UTF-8')

soup = BeautifulSoup(page, "lxml")

script_tag = str(soup.findAll('script')[5])

raw_content = script_tag.split("Spotify.Entity = ")[1].split("</script>")[0].split(";")[0]

json_content = json.loads(raw_content)

track_list = json_content["tracks"]["items"]


print("Spotify playlist : OK ")




file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
song_path = dir_path+"/songs/"
print(song_path)
#print(json.dumps(track_list, indent = 1))

nbr_of_track = len(track_list)
for track in track_list:
	#track = tracks[0]
	name = track["track"]["name"]
	artist = track["track"]["artists"][0]["name"]
	duration_s = int(track["track"]["duration_ms"]) / 1000 # ms to s
	query = name+" - "+artist
	query = query.replace("/",".")
	#duration_s = 95.142
	#query = "Long Espresso - o k h o"
	print("Search in youtube : "+query+" "+str(duration_s))

	videosSearch = VideosSearch(query, limit = 3)


	videos = videosSearch.result()["result"]

	#print(json.dumps(videos, indent = 1))


	videos2 = [x for x in videos if condition(time_conv(x["duration"]),duration_s)] # Delete "compilation" videos by deleting too long videos
	if len(videos2) == 0:
		video = videos[0]
	else:
		video = videos2[0] # Most pertinent video according to YT


	download_url = video["link"]

	print(query +" --> "+download_url)


	ydl_opts = {
		'format': 'worstaudio/worst',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
		'outtmpl' : song_path+query+'.mp3'
	}
	
	youtube_dl.YoutubeDL(ydl_opts).download([download_url])
	
	
	print("------------------- "+str((track_list.index(track) * 100) / nbr_of_track)+"% -----------------------------")
