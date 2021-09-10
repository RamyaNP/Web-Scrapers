import requests
from datetime import datetime
import json
import time
arr=[]
endcursor=''
account="officialhumansofhyderabad"
page_count=5
for i in range(0,page_count):
	url="https://www.instagram.com/{0}/?__a=1&max_id={1}".format(account,endcursor)
	r=requests.get(url)
	data=json.loads(r.text)	
	end_cursor=data["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
	edges=data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
	
	for element in edges:
		arr.append(element["node"])
	time.sleep(2)
print(end_cursor)
with open("user_posts.json","w") as outfile:
	json.dump(arr,outfile)
	
with open("user_posts.json","r") as f:
	arr=json.loads(f.read())
	
dataset=[]
i=1
for element in arr:
	shortcode=element["shortcode"]
	timestamp=element["taken_at_timestamp"]
	dtobj=datetime.fromtimestamp(timestamp)
	date=dtobj.strftime("%d/%m/%Y")
	pic_url=element["display_url"]
	response=requests.get(pic_url)
	filename="pic{0}.jpg".format(str(i))
	f=open(filename,"wb")
	f.write(response.content)
	f.close()
	i+=1
	url="https://www.instagram.com/p/{0}/?__a=1".format(shortcode)
	r=requests.get(url)
	data=json.loads(r.text)
	try:
		location=data["graphql"]["shortcode_media"]["location"]["name"]
	except:
		location=''
	dataset.append({"shortcode":shortcode,"location":location,"date":date,"picture":filename})
with open("user_data.json","w") as outfile:
	json.dump(dataset,outfile)

