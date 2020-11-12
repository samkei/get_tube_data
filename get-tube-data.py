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
        pattern = "\d{4}-[0-1][0-2]-([0-2][0-9]|[3][0-1])"
        match_nomatch = re.match(pattern, time)
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
        if go_no_go is True:
            return json_reponse
        else:
            dic = {sub["id"]: sub["snippet"]["title"] for sub in json_reponse_items}
        return dic


class Search(RequestData):
    def __init__(self, order, publishedAfter=None, publishedBefore=datetime.datetime.now(),days_before=30,q=None, type=None, topicId=None, relevanceLanguage="en"):
        super().__init__("search", "snippet")
        if publishedAfter is None:
            self.publishedAfter = str(self.get_date_n_days_before(days_before,publishedBefore)[1])
        self.order = order
        self.publishedBefore = publishedBefore
        self.f_publishedBefore = RequestData.format_system_time(str(publishedBefore))
        self.days_before = int(days_before)
        self.f_publishedAfter = self.get_date_n_days_before(days_before,publishedBefore)[0]
        self.q = q
        self.type = type
        self.topicId = topicId
        self.relavanceLanguage = relevanceLanguage
        self.default_search_publish_return_time_title_url = RequestData.build_url(self.search_type, order=self.order, part=self.part,
                                                                   publishedBefore=self.f_publishedBefore,
                                                                   publishedAfter=self.f_publishedAfter,
                                                                   relevanceLanguage=self.relavanceLanguage,
                                                                   maxResults=self.maxResults, key=self.apiKey)

        self.default_search_between_dates_return_videoIds_url = RequestData.build_url(self.search_type, order=self.order, part=self.part,
                                                                   publishedBefore=self.f_publishedBefore,
                                                                   publishedAfter=self.f_publishedAfter,
                                                                   relevanceLanguage=self.relavanceLanguage,
                                                                   maxResults=self.maxResults, key=self.apiKey)

        self.default_search_between_dates_by_days_return_videoIds_url = RequestData.build_url(self.search_type, order=self.order,
                                                                   part=self.part,
                                                                   publishedBefore=self.f_publishedBefore,
                                                                   publishedAfter=self.f_publishedAfter,
                                                                   relevanceLanguage=self.relavanceLanguage,
                                                                   maxResults=self.maxResults, key=self.apiKey)

    def get_search_snippets_return_publish_time_title(self):
        json_reponse = RequestData.build_request(self.default_search_publish_return_time_title_url)
        json_reponse_items = json_reponse["items"]
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_reponse
        else:
            dic = {sub['snippet']['publishedAt']:sub['snippet']["title"] for sub in json_reponse_items}
        return dic


    def get_search_snippets_between_dates_return_videoIds(self):
        json_reponse = RequestData.build_request(self.default_search_between_dates_return_videoIds_url)
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_reponse
        else:
            json_reponse_items = json_reponse["items"]
            json_list = [val['id']['videoId'] for val in json_reponse_items]
        return json_list


    def get_search_snippets_between_dates_by_days_return_videoIds(self):
        json_reponse = RequestData.build_request(self.default_search_between_dates_by_days_return_videoIds_url)
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_reponse
        else:
            json_reponse_items = json_reponse["items"]
            json_list = [val['id']['videoId'] for val in json_reponse_items]
        return json_list


    @classmethod
    def get_date_n_days_before(cls, rdays=None,date=datetime.datetime.now()):
        if rdays is None:
            rdays = cls.days_before
        days = int(rdays)
        delta1 = date
        delta2 = datetime.timedelta(days=+ days)
        diff = delta1 - delta2
        return RequestData.format_system_time(diff), diff


class Videos(RequestData):

    def __init__(self, id=None, chart="mostPopular", videoCategoryId="28"):
        super().__init__("videos","statistics")
        self.chart = chart
        self.videoCategoryId = videoCategoryId
        self.id = id
        self.default_video_statistics_by_videocategoryId_url = RequestData.build_url(self.search_type, part=self.part,
                                                                             chart=self.chart,
                                                                             videoCategoryId=self.videoCategoryId,
                                                                             maxResults=self.maxResults,
                                                                             key=self.apiKey)
        self.default_video_snippets_by_id_url = RequestData.build_url(self.search_type, part="snippet",
                                                                             id=self.id,
                                                                             maxResults=self.maxResults,
                                                                             key=self.apiKey)

    def get_video_statistics_by_videocategoryId(self):
        json_reponse = RequestData.build_request(self.default_video_statistics_by_videocategoryId_url)
        json_reponse_items = json_reponse["items"]
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_reponse
        else:
            for item in json_reponse_items:
                dic = {sub['id']: sub['statistics']['likeCount'] for sub in json_reponse_items}
        return dic


    def get_video_snippets_by_id(self):
        json_reponse = RequestData.build_request(self.default_video_snippets_by_id_url)
        json_reponse_items = json_reponse["items"]
        json_obj = json_reponse.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_reponse
        else:
            json_reponse_id_snippet = {key["id"]:key["snippet"] for key in json_reponse_items}
        return json_reponse_id_snippet


def handler(event, context):
        print(f'Retrieving the top 50 viewed youtube videos for the specified "date range." Default already set to 30 days from the current system time. From the returned Ids performing secondary query to retrieve data such as categoryId and tags relating to them.\nThis information can provide dataset for important national trends or changes in a specified period of time."')

        #For this search instance only parameter needed is "viewCount."  Default values already set in parent and child class of the instance.
        new_vid_search = Search("viewCount")

        time = RequestData.format_system_time(datetime.datetime.now())
        print(f'Current system date/time is: {time}. Retrieving items from the "search" resource between {Search.get_date_n_days_before(30,datetime.datetime.now())[0]} and the current date/time of {time}: ')

        #Instance method get_search_snippets_between_dates() can take a "published_before_date" and a "date_range" parameters. Default: "current system time" and 30 days.
        new_vid_search_response = new_vid_search.get_search_snippets_between_dates_return_videoIds()
        print(new_vid_search_response)

        print(f"These are the top 50 items returned showing their title and descriptions. Another query is needed to retrieve their categoryId and further information such as associated tags.")

        vid_ids = ",".join(new_vid_search_response)
        new_vid_snippet = Videos(id=vid_ids)
        vid_snippet_response = new_vid_snippet.get_video_statistics_by_videocategoryId()
        vid_snippet_response = new_vid_snippet.get_video_snippets_by_id()
        vid_snippet_response = RequestData.build_url("videos", part="snippet", id=vid_ids,maxResults=new_vid_snippet.maxResults, key=RequestData.apiKey)
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
