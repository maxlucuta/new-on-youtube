import googleapiclient.discovery
from bs4 import BeautifulSoup
import requests
import re
from xml.etree import ElementTree 

## I've overdone the comments for quicker handover. Feel free to take them out.

##----------------------------------------------------------------------------
## API setup
##----------------------------------------------------------------------------
API_SERVICE = "youtube"
API_VERSION = "v3"
API_KEY = "AIzaSyCEYn_Co51eJlG5sCbzVbPQ9HQn-RHxRms"

## ---------------------------------------------------------------------------
## API paramter variables
## Currently just makes one request up to max 50 results
## We'll need to implement paging in the API calls to get past the 50th result
## ---------------------------------------------------------------------------
api_results_per_page = 20
search_published_after = "2023-01-01"
search_terms = "sport|football|baseball|ice hockey|basketball"

##----------------------------------------------------------------------------
## API call
##----------------------------------------------------------------------------
youtube = googleapiclient.discovery.build(
    API_SERVICE, API_VERSION, developerKey = API_KEY)

request = youtube.search().list(
    part ="snippet"
    , publishedAfter = search_published_after + "T00:00:00Z"
    , q = search_terms
    , maxResults = api_results_per_page
    , type = "video"
    , regionCode = "gb"
    , safeSearch = "moderate"
    , videoDuration = "medium"
    ## , videoEmbeddable = "true"
    , videoCaption = "closedCaption"
)

response = request.execute()

##----------------------------------------------------------------------------
## Iterate through videos in the API response and populate a list ('videos')
## with a dict of information for each video (including transcript text)
##----------------------------------------------------------------------------
videos = []

for item in response['items']:
    video_id = item['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    ## Get the source for the vido pages
    html = requests.get(video_url)
    soup = BeautifulSoup(html.text,'html.parser')

    ## Extract the contents of all style tags
    script_text = [tag.string for tag in soup.find_all('script') if tag.string != None]

    ## Find all quote enclosed urls and deduplicate them
    urls = set()
    pattern = re.compile(r'"(http.*?)"')

    ## Extract and correct URLs containing "timedtext"
    ## i.e. https://www.youtube.com/api/timedtext...
    for text in script_text:
        found_urls = re.findall(pattern, text)
        found_urls = {url.replace(r"\u0026", "&") for url in found_urls if "timedtext" in url}
        urls.update(found_urls)
        
    ## "timedtext" urls point to xml data containing the caption text 
    ## Get the xml and read it into a string
    transcript_string = ""
    if urls:
        ## for now arbitrarily choose 1 caption track if there are more than 1
        ## videos can have more than one track so we might want to improve the selection (e.g. length etc.)
        caption_url = list(urls)[0] 
        transcript = requests.get(caption_url)
    
        transcript_tree = ElementTree.fromstring(transcript.content)
    
        for child in transcript_tree:
            transcript_string += child.text.replace("&#39;", "'")
            transcript_string += " "
    
    ## Add API data and the caption string to the list of video dicts
    if transcript_string:
        video_dict = {'video_id': video_id
                      ,'video_url' : video_url
                      ,'video_name' : item['snippet']['title']
                      ,'channel_id' : item['snippet']['channelId']
                      ,'channel_name' : item['snippet']['channelTitle']
                      ,'video_description' : item['snippet']['description']
                      ,'etag' : item['etag']
                      ,'transcript': transcript_string
                      }
        videos.append(video_dict)
