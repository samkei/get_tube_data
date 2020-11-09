from __future__ import print_function
import re
import os
import json
import boto3
import datetime
import dateutil.parser
import requests


class RequestData:
    site = "youtube"
    version = "v3"
    apiKey = os.getenv('API_KEY')
    base_url = f"https://www.googleapis.com/{site}/{version}/"


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
        return items


    @classmethod
    def json_error_checker(cls, json_response_object_keys):
        json_response = list(json_response_object_keys)
        if "error" in json_response:
            invalid = True
        elif "items" in json_response:
            invalid = False
        return invalid


    @classmethod
    def json_loader(cls, json_file, mode="r"):
        with open(json_file, mode) as json_file_loaded:
            json_ser = json.load(json_file_loaded)
        return json_ser


    @classmethod
    def format_input_time(cls, time):
        pattern = "\d{4}-[0-1][0-2]-([0-2][0-9]|[3][0-1])"   ##"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
        match_nomatch = re.match(pattern, time) #"%Y%m%dT%H%M%S%fZ"
        if match_nomatch:
            parsed = dateutil.parser.parse(time)
            converted = str(parsed.date()) + "T" + str(parsed.time()) + "Z"
            return converted
        else:
            return "Error: could not format time string."


    @classmethod
    def format_system_time(cls, time):
        parsed = dateutil.parser.parse(str(time))
        new_time = parsed.time().strftime("%H:%M:%S")
        return str(parsed.date()) + "T" + str(new_time) + "Z"



class VideoCategories(RequestData):
    def __init__(self, regionCode="us"):
        super().__init__("videoCategories", "snippet")
        self.regionCode = regionCode
        self.default_video_snippet = RequestData.build_url(self.search_type, regionCode=self.regionCode, maxResults=self.maxResults, part=self.part, key=self.apiKey)


    def get_videoCategories_snippets(self):
        json_reponse = RequestData.build_request(self.default_video_snippet)
        json_reponse_items = json_reponse["items"]
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go == True:
            return json_reponse
        else:
            dic = {sub["id"]: sub["snippet"]["title"] for sub in json_reponse_items}
        return dic


class Search(RequestData):
    #topic_id_dic = RequestData.json_loader("topicIds.json")
    #ordered_dic = {sub[nii] for  }

    def __init__(self, order, type=None, topicId=None, publishedBefore=None,publishedAfter=None, q=None, relevanceLanguage="en"):
        super().__init__("search", "snippet")
        self.order = order
        self.topicId = topicId
        self.type = type
        self.publishedBefore = publishedBefore
        self.publishedAfter = publishedAfter
        self.q = q
        self.relavanceLanguage = relevanceLanguage
        self.default_search_by_topicId_url = RequestData.build_url(self.search_type, order=self.order,part=self.part,relevanceLanguage=self.relavanceLanguage,maxResults=self.maxResults, key=self.apiKey)


    def get_search_snippets(self):
        json_reponse = RequestData.build_request(self.default_search_by_topicId_url)
        json_reponse_items = json_reponse["items"]
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go == True:
            return json_reponse
        else:
            dic = {sub['snippet']['publishedAt']:sub['snippet']["title"] for sub in json_reponse_items}
        return dic


    def get_search_snippets_between_dates(self,published_before_date=datetime.datetime.now(),date_range=30):
        date_range_int = int(date_range)
        default_published_before_date = RequestData.format_system_time(published_before_date)
        past_month = str(self.get_date_n_days_before(date_range_int))
        vid_snippet_url = RequestData.build_url(self.search_type, part=self.part, publishedBefore=default_published_before_date,publishedAfter=past_month,maxResults=self.maxResults, key=self.apiKey)
        json_reponse = RequestData.build_request(vid_snippet_url)
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go == True:
            return json_reponse
        else:
            json_reponse_items = json_reponse["items"]
            json_list = {val['id']['videoId']:val['snippet'] for val in json_reponse_items}

        return json_list #, dic1 #f"{invalid} because {json[:10]} in array: {json_reponse}"


    @classmethod
    def get_date_n_days_before(cls, days,date=datetime.datetime.now()):
        delta1 = date
        delta2 = datetime.timedelta(days=+ days)
        diff = delta1 - delta2
        return RequestData.format_system_time(diff)


#part:contentDetails, fileDetails, id, liveStreamingDetails, localizations, player,
# processingDetails, recordingDetails, snippet, statistics, status, suggestions, topicDetails;
#chart: mostPopular; id; maxResults; pageToken; regionCode; chart
class Videos(RequestData):

    def __init__(self, chart=None, videoCategoryId=None, id=None):
        super().__init__("videos","statistics")
        self.chart = chart
        self.videoCategoryId = videoCategoryId
        self.id = id
        self.default_video_statistics_by_topicId_url = RequestData.build_url(self.search_type, chart=self.chart,part=self.part,videoCategoryId=self.videoCategoryId,maxResults=self.maxResults, key=self.apiKey)


    def get_video_statistics(self, url=self.default_video_statistics_by_topicId_url):
        json_reponse = RequestData.build_request(url)
        json_reponse_items = json_reponse["items"]
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go == True:
            return json_reponse
        else:
            for item in json_reponse_items:
                dic = {sub['id']: sub['statistics']["viewCount"] for sub in json_reponse_items}
        return dic


    def get_video_snippets_title(self):
        vid_snippet_url = RequestData.build_url(self.search_type, part="snippet", id=self.id,maxResults=self.maxResults, key=self.apiKey)
        json_reponse = RequestData.build_request(vid_snippet_url)
        json_reponse_items = json_reponse["items"]
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go == True:
            return json_reponse
        else:
            json_reponse_categoryIds = {key["categoryId"]:key["tags"] for key in json_reponse_items}
        return json_reponse_categoryIds


def handler(event, context):
        print(f'This application will retrieve the top 50 viewed youtube videos for a specified "date range," but which defaults to 30 days from the current system time. From the returned Ids a secondary query is triggerred returning alll the categories these top-viewed videos belong to.\nThis information when fully realized as the dataset is expanded can indicate important national trends or changes if any for specified periods of times."')

        new_vid_search = Search("viewCount")  # "ViewCount", category_Id, None, None, datetime.datetime.now())

        time = RequestData.format_system_time(datetime.datetime.date())
        print(f"Current system time is: {time}. Retrieving items from search resource: ")
        vid_search_response = vid_search.get_search_snippets_between_dates()
        print(vid_search_response)

        print(f"These are the top 50 items returned showing their title and descriptions. Another query is needed to retrieve their categoryId and further informatino such as associated tags.")
        vid_ids = vid_search_response.keys()

        new_vid_snippet = Videos(id=vid_ids)
        vid_snippet_response = new_vid_snippet.get_video_snippets_title()
        print(vid_snippet_response)

        '''
        #topic_ids = str([1, 2, 3, 15,])#Search.topic_id_dic
        #mydate = str(input("Enter your date please: "))
        pattern = "\d{4}-[0-1][0-2]-([0-2][0-9]|[3][0-1])" #-(\d{1.12})-\d{1.31}"
        #my_match = re.match(pattern, mydate)
        #while not my_match:
         #   mydate = str(input("Incorrect format: Please enter your date in format yyyy-mm-dd hh:ss:mm: "))
         #   my_match = re.match(pattern,mydate)

        #mydate_converted = RequestData.format_input_time(mydate)

        #user_topic_Id = str(input(f"{topic_ids}.\nPlease select a 'category Id' from this list: "))
        #while user_topic_Id not in topic_ids:
        #   user_topic_Id = str(input(f"{topic_ids}.\nYour input is not in the list. Please select a 'category Id' from this list: "))


           #ne = Search("")
        print(vid_search_response)
        '''

        #handler(None,None)
