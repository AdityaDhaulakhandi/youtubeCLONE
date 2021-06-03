from django.shortcuts import render
import requests

from django.conf import settings


app_name='channel'

def index(request):

      channel=[]

      if request.method=="POST":
            search_url='https://www.googleapis.com/youtube/v3/search'
            url_channel='https://www.googleapis.com/youtube/v3/channels'

            search_params={
                  'part':'snippet',
                  'type':'channel',
                  'q':request.POST['search'],
                  'maxResults':3,
                  'key':settings.YOUTUBE_DATA_API_KEY

            }

            r=requests.get(search_url,params=search_params)

            channel_ids=[]
            results=(r.json()['items'])
            for result in results:
                  channel_ids.append(result['snippet']['channelId'])

            channel_params={
                  'part':'snippet,statistics',
                  'id':(',').join(channel_ids),
                  'maxResults':3,
                  'order':'viewCount',
                  'key':settings.YOUTUBE_DATA_API_KEY

            }

            r=requests.get(url_channel,params=channel_params)


            results=(r.json()['items'])

            for result in results:
                  
                  channel_data={
                  'title':result['snippet']['title'],
                  'thumbnail': result['snippet']['thumbnails']['medium']['url'],
                  'viewCount': result['statistics']['viewCount'],
                  'subsCount': result['statistics']['subscriberCount'],
                  'videoCount':result['statistics']['videoCount'],
                  'url':f'https://www.youtube.com/channel/{result["id"]}',
                  }
                  channel.append(channel_data)
      context={
      'channels':channel
      }      

      return render(request,'channel/index.html',context)
