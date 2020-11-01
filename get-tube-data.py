from __future__ import print_function
import os
import json
import boto3
import datetime
import requests
import googleapiclient.discovery
import googleapiclient.errors


'''
    current = datetime.datetime.now()
    delta1 = datetime.date(current.year,current.month,current.day)
    delta2 = datetime.date(year=2021,month=10,day=9)
    diff = delta1 - delta2
    print(diff)
    #ata_query_array =  data_query.strip()

    #print(data_query_array)
'''

class RequestData:
    site = "youtube"
    version = "v3"
    apiKey = os.getenv('API_KEY')
    base_url = f"https://www.googleapis.com/{site}/{version}/"
    #base_url = googleapiclient.discovery.build(site,version,credentials=apiKey)


    def __init__(self, search_type, part, pageToken=None, maxResults="50"):
        self.search_type = search_type
        self.part = part
        self.maxResults = maxResults
        self.pageToken = pageToken

    @classmethod
    def build_url(cls, main_var, **kwargs):
        items=[]
        for key, value in kwargs.items():
            items.append(key+"="+value)
            joined = "&".join(items)
        complete = cls.base_url+main_var+"?"+joined
        return complete

    @classmethod
    def build_request(cls, url):
        items = json.loads(requests.get(url).text)
        all_categories = items["items"]
        return all_categories
        # category_title = items["items"][0]["snippet"]["title"]


class VideoCategories(RequestData):
    def __init__(self, regionCode="us"):
        super().__init__("videoCategories", "snippet")
        self.regionCode = regionCode
        self.default_video_snippet = RequestData.build_url(self.search_type, regionCode=self.regionCode, maxResults=self.maxResults, part=self.part, key=self.apiKey)


    def get_videoCategories_snippets(self):
        json_reponse = RequestData.build_request(self.default_video_snippet)
        dic = {sub["id"]: sub["snippet"]["title"] for sub in json_reponse}
        return dic

#order: date, rating, relevance, title, videoCount, viewCount; pageToken: string; publishedAfter; publishedAfter;
#videoCategoryId; videoDuration; , relatedToVideoId, channelId, channelType,, type, safeSearch,;
class Search(RequestData):
    def __init__(self, order, topicId, type, q=None, relevanceLanguage="en"):
        super().__init__("search", "snippet")
        self.order = order
        self.topicId = topicId
        self.q = q
        self.relavanceLanguage = relevanceLanguage
        self.default_search_by_topicId_url = RequestData.build_url(self.search_type, order=self.order,part=self.part,topicId=self.topicId,relevanceLanguage=self.relavanceLanguage,maxResults=self.maxResults, key=self.apiKey)


    def get_search_snippets(self):
        json_reponse = RequestData.build_request(self.default_search_by_topicId_url)
        for item in json_reponse:
            dic = {sub['snippet']['publishedAt']:sub['snippet']["title"] for sub in json_reponse}
        return dic


    def get_search_snippets(self):
        json_reponse = RequestData.build_request(self.default_search_by_topicId_url)
        for item in json_reponse:
            dic = {sub['snippet']['publishedAt']: sub['snippet']["title"] for sub in json_reponse}
        return dic


#part:contentDetails, fileDetails, id, liveStreamingDetails, localizations, player,
# processingDetails, recordingDetails, snippet, statistics, status, suggestions, topicDetails;
#chart: mostPopular; id; maxResults; pageToken; regionCode; chart
class Videos(RequestData):
    #VideoCategories
    def __init__(self, chart, videoCategoryId, id=None,):
        super().__init__("video","statistics")
        self.chart = chart
        self.videoCategoryId = videoCategoryId
        self.id = id


def amain():
    tube = Search("viewCount","/m/07c1v", "en")
    topic_search = Search("viewCount","06bvp", "en")
    build = tube.base_url
    req = build.search().list(order="viewCount",TopicId="06bvp", revelanceLanguage="en")
    print(req.execute)


def main():
    tube = Search("viewCount","/m/07c1v", "en")

    #full_url = tube.build_url("search",order=tube.order,part=tube.part,topicId=tube.topicId,relevanceLanguage=tube.relavanceLanguage,maxResults=tube.maxResults,key=tube.apiKey)

    vid_cat = VideoCategories()
    vid_response = vid_cat.get_videoCategories_snippets()
    vid_response1 = tube.get_search_snippets()
    #url = vid_cat.build_url("videoCategories", region=self.region, part=self.part)

    #try:
     #   req =  vid_response #requests.get(vid_url)
        #tube = googleapiclient.discovery.build(tube_api, tube_version, developerKey = creds)
    #except Exception as e:
    #    print (f"Error {type(e)} occurred: e.args")


   # try:
       # query_response = json.loads(req.text)
    #except Exception as e:
     #   print(f"Well, another error: now error {type(e)} occurred due to {e.args}")

    #query_items = query_response["items"]
    #no_of_items = len(query_items)
    #for key, value in
    #print(tube.get_keys(query_items,no_of_items,"snippet","title"))
    #print(tube.get_keys(query_items, no_of_items, "snippet", "publishedAt"))


    print(vid_response, vid_response1)
    #print(no_of_items)
    #print(serialized)





if __name__ == '__main__':
    main()