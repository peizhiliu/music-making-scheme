import time
import re
import requests
import os
from pytube import YouTube


os.chdir("data/")

seed = "m_qlgFQs7E4"
urls = [seed]

for url_short in urls:
	#print("{}\t{}".format(url_short, urls))
	url = "https://youtube.com/watch?v={}".format(url_short)
	# download the video (if appropriate)
	try:	
		yt = YouTube(url)
	except:
		continue
	# 60 seconds, 10 minutes: that is, we want the video to be under 10 minutes (no playlists)
	# also make sure we arent trying to download a livestream (length 0)
	if yt.length <= 1*60*10 and yt.length > 0:
		if os.path.exists(url_short+".webm"):
			print("Already downloaded! " + url_short)
			time.sleep(2)
		else:
			try:
				yt.streams.filter(only_audio=True, subtype="webm").order_by("abr").desc().first().download(filename=url_short)
				# write metadata to a file
				with open(url_short+".txt", "w+") as f:
					f.write(str(yt.keywords))
				print("Downloaded! " + url_short)
			except:
				pass
			time.sleep(20)
	else:
		print("Video too long! " + url_short)
	
	# grab all the other videos on the page and add them to the crawler
	try:	
		r = requests.get(url).text
	except:
		pass	
	unparsed_urls = re.findall(r'{"url":"\/watch\?v=((\S){11})",', r)
	for u in unparsed_urls:
		if u[0] not in urls:	
			urls.append(u[0])

	# keep the tree from growing too big
	if len(urls) > 1000:
		urls = urls[980:]
