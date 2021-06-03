import requests
from isodate import parse_duration

from django.shortcuts import render, redirect
from django.conf import settings


app_name="search"

def index(request):

      videos=[]

      if request.method=='POST':
            search_url='https://www.googleapis.com/youtube/v3/search'
            search_video='https://www.googleapis.com/youtube/v3/videos'

            param_search={
                  'part':'snippet',
                  'q':request.POST['search'],
                  'maxResults':9,
                  'type':'video',
                  'key':settings.YOUTUBE_DATA_API_KEY
            }

            r=requests.get(search_url, params=param_search)
            
            # GETTING THE VIODEID OF THE 9 THUMBNAILS
            video_id=[]
            results=(r.json()['items'])
            for result in results:
                  video_id.append(result['id']['videoId'])


            if request.POST['submit'] =='feeling':
                  return redirect(f'https://www.youtube.com/watch?v={video_id[0]}')
      
            video_param={
                  'part':'snippet, contentDetails',
                  'id':','.join(video_id),
                  'maxResults':9,
                  'key':settings.YOUTUBE_DATA_API_KEY
            }

            r=requests.get(search_video,params=video_param)

            
            # VIDEO TITLE, VIDEO THUMBNAIL, VIDEO URL, VIDEO DURATION
            # video_info={
            #       'title':results_video['title']

            # }
            results_video=(r.json()['items'])
            for result in results_video:
                  video_data={
                  'title': result['snippet']['title'],
                  'id': result['id'],
                  'url':f'https://www.youtube.com/watch?v={result["id"]}',
                  'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                  'thumbnail': result['snippet']['thumbnails']['high']['url']
                  }
                  videos.append(video_data)
            
      context={
            'video':videos
      }

      return render(request,'search/index.html',context)