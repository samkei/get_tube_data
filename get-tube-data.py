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


<<<<<<< HEAD
    def put_dynamodb_item(table, id, body):
        dynamo = boto3.resource('dynamo')
        Table = dynamo.table(table)




=======
>>>>>>> 851d1778427d899933d52117f34a18530a15b3f5
class VideoCategories(RequestData):
    def __init__(self, regionCode="us"):
        super().__init__("videoCategories", "snippet")
        self.regionCode = regionCode
        self.default_video_snippet = RequestData.build_url(self.search_type, regionCode=self.regionCode, maxResults=self.maxResults, part=self.part, key=self.apiKey)


    def get_videoCategories_snippets(self):
        json_response = RequestData.build_request(self.default_video_snippet)
        json_response_items = json_response["items"]
        json_obj = json_response.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_response
        else:
            dic = {sub["id"]: sub["snippet"]["title"] for sub in json_response_items}
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
        json_response = RequestData.build_request(self.default_search_publish_return_time_title_url)
        json_response_items = json_response["items"]
        json_obj = json_response.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_response
        else:
            dic = {sub['snippet']['publishedAt']:sub['snippet']['title'] for sub in json_response_items}
        return dic


    def get_search_snippets_between_dates_return_videoIds(self):
        json_response = RequestData.build_request(self.default_search_between_dates_return_videoIds_url)
        json_obj = json_response.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_response
        else:
            json_response_items = json_response['items']
<<<<<<< HEAD
=======
            #json_response_items = [{'kind': 'youtube#searchResult', 'etag': 'L-UkMif8DgSzRpY14K05WMXmMM0', 'id': {'kind': 'youtube#video', 'videoId': 'UoI9riNffEU'}, 'snippet': {'publishedAt': '2020-11-03T09:00:12Z', 'channelId': 'UCuhAUMLzJxlP1W7mEk0_6lA', 'title': '[MV] 마마무 (MAMAMOO) - AYA', 'description': '[MV] 마마무 (MAMAMOO) - AYA Instagram: https://bit.ly/2TrQPJD Facebook: https://bit.ly/2OYoA1W Twitter: https://bit.ly/2TuKNbo About MAMAMOO. MAMAMOO( ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/UoI9riNffEU/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/UoI9riNffEU/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/UoI9riNffEU/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'MAMAMOO', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-03T09:00:12Z'}}, {'kind': 'youtube#searchResult', 'etag': '9GkRYb2WwaL9cfRh9Ko4H8OzuuQ', 'id': {'kind': 'youtube#video', 'videoId': 'AZfUpYAxPgc'}, 'snippet': {'publishedAt': '2020-11-02T08:30:49Z', 'channelId': 'UCFcBAGR0drI3F15EhMFjuTg', 'title': 'CHOCOLATE SWITCHUP CHALLENGE | Funny chocolate challenge | Aayu and Pihu Show', 'description': 'Download Duolingo For Free - https://app.adjust.com/bcxke71 Learn English and 20+ foreign languages. Aayu and Pihu enjoyed a lot during this comedy ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/AZfUpYAxPgc/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/AZfUpYAxPgc/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/AZfUpYAxPgc/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Aayu and Pihu Show', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-02T08:30:49Z'}}, {'kind': 'youtube#searchResult', 'etag': 'SO9JVCRPCsD9PWS_3ma9jlIxIos', 'id': {'kind': 'youtube#video', 'videoId': '3fqykLE2tP0'}, 'snippet': {'publishedAt': '2020-11-01T20:20:54Z', 'channelId': 'UCzYfz8uibvnB7Yc1LjePi4g', 'title': 'Among Us CHEATING GONE 100% PERFECT!', 'description': 'Become a super awesome YouTube Member! https://www.youtube.com/aphmaugaming/join Come at a look at my merch!', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/3fqykLE2tP0/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/3fqykLE2tP0/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/3fqykLE2tP0/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Aphmau', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-01T20:20:54Z'}}, {'kind': 'youtube#searchResult', 'etag': 'SGRAS2wRNgkG8oIdTGHaksPuKpY', 'id': {'kind': 'youtube#video', 'videoId': 'f21KrWqxJqM'}, 'snippet': {'publishedAt': '2020-11-03T04:00:02Z', 'channelId': 'UCP7Gw_YZAuh4Yg2fcdcuumQ', 'title': 'ARASHI - Party Starters [Official Music Video]', 'description': '2020.10.30 Release「Party Starters」 https://smarturl.it/ARASHIPartyStarters Written by Sam Hollander, Grant Michaels, Funk Uchino Rap by Sho Sakurai ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/f21KrWqxJqM/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/f21KrWqxJqM/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/f21KrWqxJqM/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'ARASHI', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-03T04:00:02Z'}}, {'kind': 'youtube#searchResult', 'etag': 'xR7DHWQH9LNQk7N_eAOWxxuX5UM', 'id': {'kind': 'youtube#video', 'videoId': 'vWdjqdmFHxw'}, 'snippet': {'publishedAt': '2020-11-03T14:00:20Z', 'channelId': 'UCJHA_jMfCvEnv-3kRjTCQXw', 'title': 'Binging with Babish: Brie &amp; Butter Baguettes from Twin Peaks', 'description': "This week we're headed back to Twin Peaks WA, but for once, not with murder on the mind. Instead, we're focusing on the food: brie and baguette sandwiches, ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/vWdjqdmFHxw/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/vWdjqdmFHxw/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/vWdjqdmFHxw/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Babish Culinary Universe', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-03T14:00:20Z'}}, {'kind': 'youtube#searchResult', 'etag': 'tkqum29_ajnqVnVe46Zzuu5Vq8Y', 'id': {'kind': 'youtube#video', 'videoId': '2oysDxhHEEk'}, 'snippet': {'publishedAt': '2020-11-03T11:00:00Z', 'channelId': 'UCXGR70CkW_pXb8n52LzCCRw', 'title': '$456 McDonald&#39;s McRib Taste Test | Fancy Fast Food', 'description': "Today, Josh and Rhett are fancifying McDonald's McRib. Fancy Fast Food Ep.11 Subscribe to Mythical Kitchen: ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/2oysDxhHEEk/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/2oysDxhHEEk/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/2oysDxhHEEk/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Mythical Kitchen', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-03T11:00:00Z'}}, {'kind': 'youtube#searchResult', 'etag': 'dMtq78RzDA5j32Wv0S4yhpvWFPc', 'id': {'kind': 'youtube#video', 'videoId': 'mU8jD9qhZ1o'}, 'snippet': {'publishedAt': '2020-10-12T15:59:55Z', 'channelId': 'UCA2JXudRGbXkAwxVL0F0lBQ', 'title': 'Roshan Digital Account', 'description': 'UBL - the best Digital Bank in Pakistan along with State Bank of Pakistan offers UBL Roshan Digital Account for overseas Pakistanis. Visit now at ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/mU8jD9qhZ1o/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/mU8jD9qhZ1o/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/mU8jD9qhZ1o/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'UBL', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T15:59:55Z'}}, {'kind': 'youtube#searchResult', 'etag': 'KibduUmIQWhxqdCEe1li6KZvuL0', 'id': {'kind': 'youtube#video', 'videoId': 'mRpW17xQf84'}, 'snippet': {'publishedAt': '2020-11-01T22:27:27Z', 'channelId': 'UCNAf1k0yIjyGu3k9BwAg3lg', 'title': 'Gary Neville outlines the problems at Manchester United &amp; suggests solutions', 'description': 'SUBSCRIBE ▻ http://bit.ly/SSFootballSub PREMIER LEAGUE HIGHLIGHTS ▻ http://bit.ly/SkySportsPLHighlights Gary Neville shares his thoughts on ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/mRpW17xQf84/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/mRpW17xQf84/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/mRpW17xQf84/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Sky Sports Football', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-01T22:27:27Z'}}, {'kind': 'youtube#searchResult', 'etag': 'WlaSmUaU1tddv1kW9MpGDf5Nu8E', 'id': {'kind': 'youtube#video', 'videoId': 'AgcS-Kvx4LY'}, 'snippet': {'publishedAt': '2020-11-03T15:30:00Z', 'channelId': 'UCdtXPiqI2cLorKaPrfpKc4g', 'title': 'Prince Harry’s Family Is DISAPPOINTED They Won’t See Archie for Christmas', 'description': "A source close to Prince Harry and Meghan Markle tells ET it's 'fully anticipated' that the couple will be home in California, rather than returning to the U.K. for ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/AgcS-Kvx4LY/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/AgcS-Kvx4LY/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/AgcS-Kvx4LY/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Entertainment Tonight', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-03T15:30:00Z'}}, {'kind': 'youtube#searchResult', 'etag': 'o3s5cp3ipBsHgnQTlI5hXcT65oY', 'id': {'kind': 'youtube#video', 'videoId': 'fTeiGAfWR4k'}, 'snippet': {'publishedAt': '2020-10-13T15:01:36Z', 'channelId': 'UCPy63SdydWJ0WBwhCQ_F-jA', 'title': 'A NIGHT AT THE MALL, MALL OF THE EMIRATES WORLD OF FASHION 2020', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/fTeiGAfWR4k/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/fTeiGAfWR4k/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/fTeiGAfWR4k/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Mall of the Emirates, Dubai', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-13T15:01:36Z'}}, {'kind': 'youtube#searchResult', 'etag': 'xhgSEbdFc2zAtHkvoEcgO48HKh4', 'id': {'kind': 'youtube#video', 'videoId': '_rTx6Ir4Zrk'}, 'snippet': {'publishedAt': '2020-10-12T23:20:37Z', 'channelId': 'UCn6aOPv5xIPaQa_0nku5HuA', 'title': 'Bota Box: Freshness 2020', 'description': 'This Is How We Bota Find out where to pick up your Bota Box: www.botabox.com Find us on social media: https://www.instagram.com/botabox/ ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/_rTx6Ir4Zrk/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/_rTx6Ir4Zrk/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/_rTx6Ir4Zrk/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Bota Box', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T23:20:37Z'}}, {'kind': 'youtube#searchResult', 'etag': 'DFtWcuiixkaHDsGmHwyPMOVTga0', 'id': {'kind': 'youtube#video', 'videoId': 'axm795geqCg'}, 'snippet': {'publishedAt': '2020-11-03T00:06:57Z', 'channelId': 'UCqZQlzSHbVJrwrn5XvzrzcA', 'title': 'Leeds United v. Leicester City | PREMIER LEAGUE HIGHLIGHTS | 11/2/2020 | NBC Sports', 'description': 'Leicester City were clinical at Elland Road, killing off a Leeds surge and grabbing a comfortable win to move into second place. #NBCSports #PremierLeague ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/axm795geqCg/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/axm795geqCg/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/axm795geqCg/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'NBC Sports', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-03T00:06:57Z'}}, {'kind': 'youtube#searchResult', 'etag': '36kpKaH860-X3xwYS3GnLgRo-wo', 'id': {'kind': 'youtube#video', 'videoId': '3nquIi7xyvk'}, 'snippet': {'publishedAt': '2020-11-03T21:59:52Z', 'channelId': 'UCuVPpxrm2VAgpH3Ktln4HXg', 'title': 'Robocop (1987)', 'description': "There's a new law enforcer in town…and he's half man, half machine! From director Paul Verhoeven comes this classic, high-powered, sci-fi fantasy about an ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/3nquIi7xyvk/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/3nquIi7xyvk/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/3nquIi7xyvk/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-03T21:59:52Z'}}, {'kind': 'youtube#searchResult', 'etag': 'fkOpM6iHDi9B4_6-ce7bwGt3PqM', 'id': {'kind': 'youtube#video', 'videoId': 'pQ5Pw3yd8j4'}, 'snippet': {'publishedAt': '2020-10-13T00:32:39Z', 'channelId': 'UCW-Dq_-R7WxTYT5PkagWdYQ', 'title': '#Belinda anuncia que esta preparando una sorpresa 🤩✨', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/pQ5Pw3yd8j4/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/pQ5Pw3yd8j4/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/pQ5Pw3yd8j4/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Ilse A.', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-13T00:32:39Z'}}, {'kind': 'youtube#searchResult', 'etag': 'yCgQFOInTa57z2CkOM9iq77zpSM', 'id': {'kind': 'youtube#video', 'videoId': '8IL9paAgrqo'}, 'snippet': {'publishedAt': '2020-10-12T17:55:04Z', 'channelId': 'UCehbuSe95DZvCNsBKvxtr_g', 'title': 'Maria&#39;s Testimonial', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/8IL9paAgrqo/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/8IL9paAgrqo/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/8IL9paAgrqo/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Tom Reed for Congress', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T17:55:04Z'}}, {'kind': 'youtube#searchResult', 'etag': 'QgtlKBQOZTOl7mFXiYr4KhNrjQc', 'id': {'kind': 'youtube#video', 'videoId': 'IrPmdjrm8QM'}, 'snippet': {'publishedAt': '2020-10-12T22:15:17Z', 'channelId': 'UCGw9WjrkCRzzqTLBym5cfvA', 'title': 'Ahorra con Vanish(R)', 'description': 'Ahorra con Vanish(R), encuentra la botella de 925mL a precio de la Bolsa 800mL.', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/IrPmdjrm8QM/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/IrPmdjrm8QM/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/IrPmdjrm8QM/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Vanish Centroamérica', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T22:15:17Z'}}, {'kind': 'youtube#searchResult', 'etag': 'Y7l87S4RH3RcQTbS86zsm796rr8', 'id': {'kind': 'youtube#video', 'videoId': 'mRue0zLckD0'}, 'snippet': {'publishedAt': '2020-10-12T14:49:16Z', 'channelId': 'UCCmRiTdh51_n9qRE0UzuN_Q', 'title': 'Actualiza tus datos', 'description': 'Actualiza tus datos incluyendo un correo electrónico para que recibas tu estado de cuenta todos los meses y estemos siempre contigo. Haz clic en el enlace en ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/mRue0zLckD0/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/mRue0zLckD0/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/mRue0zLckD0/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'AFP Crecer', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T14:49:16Z'}}, {'kind': 'youtube#searchResult', 'etag': 'VpSeLlSp9blzpF3772j1S_qxM0E', 'id': {'kind': 'youtube#video', 'videoId': 'a_AQD15SbWg'}, 'snippet': {'publishedAt': '2020-10-13T01:00:01Z', 'channelId': 'UCgLXrOlt3JkwHNOBNUlJktQ', 'title': 'Rosemary Salt Ribeye!', 'description': 'This Cowboy Ribeye steak was seasoned with Rosemary Salt and reverse seared to a perfect internal temperature of 128 #Shorts.', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/a_AQD15SbWg/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/a_AQD15SbWg/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/a_AQD15SbWg/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Groark Boys’ BBQ', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-13T01:00:01Z'}}, {'kind': 'youtube#searchResult', 'etag': '1gdMAYYHYpMjVFXE8Num3lDqqbM', 'id': {'kind': 'youtube#video', 'videoId': 'eUlzTvfdTys'}, 'snippet': {'publishedAt': '2020-11-06T21:00:09Z', 'channelId': 'UC8CqGX45auXOKALWrr_G9VQ', 'title': 'Haikyu!! Abridged Pilot!', 'description': 'Huge shoutout and thank you to dave on Patreon for suggesting this~ Follow the Schmuck Squad on Twitter to get your daily abridged news! Also check out our ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/eUlzTvfdTys/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/eUlzTvfdTys/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/eUlzTvfdTys/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'The Schmuck Squad', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-06T21:00:09Z'}}, {'kind': 'youtube#searchResult', 'etag': 'VTpr1ELzCz7ZnVAPgV2mJic9BDU', 'id': {'kind': 'youtube#video', 'videoId': 'P0uYRs_-vso'}, 'snippet': {'publishedAt': '2020-10-12T15:08:21Z', 'channelId': 'UCb3HLWA-E4YpRTxyrNaNUGA', 'title': 'Vote for Thom Tillis | Protect Your Freedom | AFP Action', 'description': "Get Voting Info at VoteForTillis.com *** Paid for by Americans for Prosperity Action. Not authorized by any Candidate or Candidate's Committee. www.", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/P0uYRs_-vso/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/P0uYRs_-vso/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/P0uYRs_-vso/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'AFP Action', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T15:08:21Z'}}, {'kind': 'youtube#searchResult', 'etag': 'in60jwiGZImsHaWE5coH3a_V2w4', 'id': {'kind': 'youtube#video', 'videoId': 'udZNjnnDbDA'}, 'snippet': {'publishedAt': '2020-11-07T10:35:41Z', 'channelId': 'UCX2dNdYesTrOC7tjiQs9jHA', 'title': 'Coming soon.', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/udZNjnnDbDA/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/udZNjnnDbDA/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/udZNjnnDbDA/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Garena Call of Duty Mobile', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-07T10:35:41Z'}}, {'kind': 'youtube#searchResult', 'etag': '0-xlu1hFNtwW-uYMsLcHmbIkwwE', 'id': {'kind': 'youtube#video', 'videoId': 'VPxOWXMgGYM'}, 'snippet': {'publishedAt': '2020-11-10T01:00:12Z', 'channelId': 'UCvX6SymQRQ9pYEpaRWEExRA', 'title': 'QUE OSO SE ECHÓ JESSICA! Lavó la gallina y la dejo con pelos🤣 Nayeli va muy bien con su menú. P 16', 'description': 'SUSCRIBETE es FACIL http://goo.gl/aLNQ6X IMPORTANTE (No olvides dejar la activada para recibir notificaciones) Siguenos en Facebook ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/VPxOWXMgGYM/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/VPxOWXMgGYM/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/VPxOWXMgGYM/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'El Salvador 4K', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-10T01:00:12Z'}}, {'kind': 'youtube#searchResult', 'etag': 'cEcMZwoV3NbPM8YuqkHXXnQ3tpo', 'id': {'kind': 'youtube#video', 'videoId': 'kkgjw6zf7Qk'}, 'snippet': {'publishedAt': '2020-10-12T15:18:34Z', 'channelId': 'UCwx7ggTO2ne-mORSVONryiQ', 'title': 'Crayola Washimals', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/kkgjw6zf7Qk/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/kkgjw6zf7Qk/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/kkgjw6zf7Qk/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Crayola UK', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T15:18:34Z'}}, {'kind': 'youtube#searchResult', 'etag': '4XBprI_A1xaTnuJBwq2v4yfcj8c', 'id': {'kind': 'youtube#video', 'videoId': 'Nr9ORHITEKE'}, 'snippet': {'publishedAt': '2020-11-01T07:00:02Z', 'channelId': 'UCC7QOlwrWzQyOlZ1zpjOSjg', 'title': 'American Ninja 3: Blood Hunt', 'description': 'The enormously popular American Ninja series continues with this latest installment of non-stop martial arts wizardry, international intrigue and blazing Ninja ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/Nr9ORHITEKE/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/Nr9ORHITEKE/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/Nr9ORHITEKE/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-01T07:00:02Z'}}, {'kind': 'youtube#searchResult', 'etag': 'K2xVeUIcUNB9-fWVZsuXq5tP-tY', 'id': {'kind': 'youtube#video', 'videoId': 'jQWwFclQpKA'}, 'snippet': {'publishedAt': '2020-11-06T17:59:52Z', 'channelId': 'UCC7QOlwrWzQyOlZ1zpjOSjg', 'title': 'Man of Tai Chi', 'description': 'Keanu Reeves makes his directorial debut in this explosive marital arts drama that reunites him with legendary Matrix Trilogy fight choreographer Yuen Wo Ping ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/jQWwFclQpKA/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/jQWwFclQpKA/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/jQWwFclQpKA/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-06T17:59:52Z'}}, {'kind': 'youtube#searchResult', 'etag': 'T-lshY6ZGCP2Il9AcDEFkkutDCo', 'id': {'kind': 'youtube#video', 'videoId': 'BZPBZjexprY'}, 'snippet': {'publishedAt': '2020-11-09T00:00:10Z', 'channelId': 'UCk44YAELxu3FHf3Fu56x2fg', 'title': 'Sueño frustrado de Bessy🥺 Kuaky agradeció a los suscriptores que hicieron realidad sus sueños🤗 P 12', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/BZPBZjexprY/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/BZPBZjexprY/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/BZPBZjexprY/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Cocinando con El Salvador 4K', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-09T00:00:10Z'}}, {'kind': 'youtube#searchResult', 'etag': 'IQZVkNLX1WXyBAXcqTR6BmVjvVk', 'id': {'kind': 'youtube#video', 'videoId': 'cJXHi_HWdec'}, 'snippet': {'publishedAt': '2020-11-08T21:00:11Z', 'channelId': 'UCvX6SymQRQ9pYEpaRWEExRA', 'title': 'JESSICA DICE QUE SU MAMÁ YA LA ORIENTO PARA HACER LOS PANES👏 Deisy tambien anda preocupada🤔 Part 8', 'description': 'SUSCRIBETE es FACIL http://goo.gl/aLNQ6X IMPORTANTE (No olvides dejar la activada para recibir notificaciones) Siguenos en Facebook ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/cJXHi_HWdec/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/cJXHi_HWdec/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/cJXHi_HWdec/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'El Salvador 4K', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-08T21:00:11Z'}}, {'kind': 'youtube#searchResult', 'etag': 'pKbh9UBpop3xdykQfVyJzsDCLRU', 'id': {'kind': 'youtube#video', 'videoId': 'iCfSymus9o8'}, 'snippet': {'publishedAt': '2020-10-12T15:45:54Z', 'channelId': 'UCxgESilqi4R88rtzN8nanSA', 'title': 'SEAT ARONA  - Griffe FR chez Seat Guyane, Sud Motors', 'description': 'La griffe FR de la gamme Seat, qui mieux que Naubert pour vous en parler ... Pour en savoir +, rendez-vous en concession ou sur https://bit.ly/2GHi80T.', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/iCfSymus9o8/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/iCfSymus9o8/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/iCfSymus9o8/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Seat Guyane', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T15:45:54Z'}}, {'kind': 'youtube#searchResult', 'etag': 'wWQHOOlEWGzhboI34Y2t6DdnY6o', 'id': {'kind': 'youtube#video', 'videoId': 'mqkEotfPzqY'}, 'snippet': {'publishedAt': '2020-11-07T19:00:09Z', 'channelId': 'UCvX6SymQRQ9pYEpaRWEExRA', 'title': 'LAS CHICAS LLEGARON AL MERCADO! QUE OSO SE ECHÓ LAURA🤣 Bessy: hoy no anda Camaron puedo gritar. P 3', 'description': 'SUSCRIBETE es FACIL http://goo.gl/aLNQ6X IMPORTANTE (No olvides dejar la activada para recibir notificaciones) Siguenos en Facebook ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/mqkEotfPzqY/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/mqkEotfPzqY/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/mqkEotfPzqY/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'El Salvador 4K', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-07T19:00:09Z'}}, {'kind': 'youtube#searchResult', 'etag': 'T8UF_9dSk0qi2ySn6eWORszDwqY', 'id': {'kind': 'youtube#video', 'videoId': 'HYOH-cdg7kw'}, 'snippet': {'publishedAt': '2020-11-07T21:00:09Z', 'channelId': 'UCvX6SymQRQ9pYEpaRWEExRA', 'title': 'NAYELI ANDA PREOCUPADA POR QUE NO SABE HACER TAMALES😬 Bessy andaba comprando y sin dinero🤣 Parte 4', 'description': 'SUSCRIBETE es FACIL http://goo.gl/aLNQ6X IMPORTANTE (No olvides dejar la activada para recibir notificaciones) Siguenos en Facebook ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/HYOH-cdg7kw/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/HYOH-cdg7kw/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/HYOH-cdg7kw/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'El Salvador 4K', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-07T21:00:09Z'}}, {'kind': 'youtube#searchResult', 'etag': 'kY5SyPg4zY1zvBrpxToxNQPbHFA', 'id': {'kind': 'youtube#video', 'videoId': 'yppwawxWl8w'}, 'snippet': {'publishedAt': '2020-11-01T07:00:22Z', 'channelId': 'UCuVPpxrm2VAgpH3Ktln4HXg', 'title': 'Cattle Annie &amp; Little Britches', 'description': 'Annie and Jenny, a couple of wild teenagers, have a terrible disappointment upon meeting the infamous Doolin-Dalton gang. The two girls convince the group to ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/yppwawxWl8w/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/yppwawxWl8w/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/yppwawxWl8w/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-01T07:00:22Z'}}, {'kind': 'youtube#searchResult', 'etag': 'b9YzRMsqIZlKQiV-n9Kak_7UxMw', 'id': {'kind': 'youtube#video', 'videoId': 'mjPYkuo3NQg'}, 'snippet': {'publishedAt': '2020-10-13T07:18:00Z', 'channelId': 'UCUQ2arf_p0Bv3z0ctgGuIjg', 'title': 'Running out of time', 'description': 'Find out more below: Instagram: https://www.instagram.com/newhopecorpaustralia Twitter: https://www.twitter.com/newhopecorp LinkedIn: ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/mjPYkuo3NQg/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/mjPYkuo3NQg/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/mjPYkuo3NQg/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'New Hope Group', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-13T07:18:00Z'}}, {'kind': 'youtube#searchResult', 'etag': 'W-hdpANW0JngtNFPbGWoLnKO3G4', 'id': {'kind': 'youtube#playlist', 'playlistId': 'PLawOhkw2U2K9Vv0hNAusGwJYhMO1rWFvR'}, 'snippet': {'publishedAt': '2020-10-12T21:59:39Z', 'channelId': 'UCJL-S1GilHUxY_6XWc8ei7w', 'title': 'Retos', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/45ZiSAngmOA/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/45ZiSAngmOA/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/45ZiSAngmOA/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'DarekGlobal', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T21:59:39Z'}}, {'kind': 'youtube#searchResult', 'etag': 'gFNB_AANIVJaU1xN3NlneWbEZoA', 'id': {'kind': 'youtube#video', 'videoId': 'GT_dTzV60L8'}, 'snippet': {'publishedAt': '2020-11-07T19:10:19Z', 'channelId': 'UC3KdHGRjFlNmulEhLH5aXFg', 'title': 'ARK GENESIS PART 2 OFFICIAL REVEAL 😲😲', 'description': 'DONATE HERE - https://www.extra-life.org/participant/loadedcrysis Welcome to the BIG LIVESTREAM! ARK GENESIS PART 2! If you guys enjoyed this video!', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/GT_dTzV60L8/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/GT_dTzV60L8/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/GT_dTzV60L8/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'LoadedCrysis - DAILY GAMING VIDEOS AND NEWS!', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-07T19:10:19Z'}}, {'kind': 'youtube#searchResult', 'etag': '_uNuz3A3i8ENv5UqAg77d2ndqyE', 'id': {'kind': 'youtube#video', 'videoId': 'xAac0mdA98Y'}, 'snippet': {'publishedAt': '2020-11-09T12:25:33Z', 'channelId': 'UClBr7PntP6j8_vPA0RkN_kA', 'title': 'Pubg || Gap raledu ichha 🤪chit chat live with GIRL GAMER sriyt  |#Pubglive#pubgtelugugirlgamer', 'description': 'Contact Details : Youtube : https://www.youtube.com/channel/UClBr... Instagram : https://www.instagram.com/girl_gamer_sriyt Discord ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/xAac0mdA98Y/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/xAac0mdA98Y/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/xAac0mdA98Y/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'GIRL GAMER - SRI YT', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-09T12:25:33Z'}}, {'kind': 'youtube#searchResult', 'etag': '8Y1Ob-FDxih6vs7rjfcpa4cEz3s', 'id': {'kind': 'youtube#video', 'videoId': 'lvNpecjukmk'}, 'snippet': {'publishedAt': '2020-11-01T07:00:03Z', 'channelId': 'UCuVPpxrm2VAgpH3Ktln4HXg', 'title': 'Count Yorga, Vampire', 'description': 'Count Yorga, a Bulgarian vampire, departs the old world for sunny southern California. He settles in suburbia, in a stone and cobweb gothic mansion, ans starts ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/lvNpecjukmk/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/lvNpecjukmk/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/lvNpecjukmk/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-01T07:00:03Z'}}, {'kind': 'youtube#searchResult', 'etag': 'cKocBsiKQuOpDzioKnbHMevDW-0', 'id': {'kind': 'youtube#video', 'videoId': 'DMYGDwqmFqk'}, 'snippet': {'publishedAt': '2020-10-24T16:03:20Z', 'channelId': 'UCy1Ir3xKCq35ebjX-bN6Z6g', 'title': 'Godzilla: King Of The Monsters', 'description': 'The story follows the heroic efforts of the crypto-zoological agency Monarch as its members face off against a battery of god-sized monsters, including the mighty ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/DMYGDwqmFqk/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/DMYGDwqmFqk/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/DMYGDwqmFqk/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-24T16:03:20Z'}}, {'kind': 'youtube#searchResult', 'etag': 'f8wVDBKdPIO7xup0hdtQpFTahJ4', 'id': {'kind': 'youtube#video', 'videoId': 'mvfjjQsCB0o'}, 'snippet': {'publishedAt': '2020-10-28T04:02:03Z', 'channelId': 'UCjaEmLwYycKpudfDPw1yRYQ', 'title': 'Blumhouse&#39;s the Craft: Legacy', 'description': "In Blumhouse's continuation of the cult hit The Craft, an eclectic foursome of aspiring teenage witches get more than they bargained for as they lean into their ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/mvfjjQsCB0o/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/mvfjjQsCB0o/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/mvfjjQsCB0o/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-28T04:02:03Z'}}, {'kind': 'youtube#searchResult', 'etag': '8joKivdG_FmByyWNFu9ZFUplGkI', 'id': {'kind': 'youtube#video', 'videoId': '-oiAMM2DL_M'}, 'snippet': {'publishedAt': '2020-11-08T17:15:10Z', 'channelId': 'UCcM5PZhDPAizARv79hYq4yA', 'title': 'Sernik z bezą Jak upiec świąteczny sernik żeby nie opadł', 'description': 'przepismamy #heniafoks #przepisykulinarne Jak zrobić puszysty sernik z beza na wierzchu ?! Przepis na wyjątkowo pyszny sernik pianką ! Jak upiec ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/-oiAMM2DL_M/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/-oiAMM2DL_M/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/-oiAMM2DL_M/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Henia Foks', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-08T17:15:10Z'}}, {'kind': 'youtube#searchResult', 'etag': 'xIPK3LJhbswyIlikdpFvg0YYcaI', 'id': {'kind': 'youtube#video', 'videoId': 'mSF8ZHPCWjo'}, 'snippet': {'publishedAt': '2020-11-08T13:37:19Z', 'channelId': 'UCiWrjBhlICf_L_RK5y6Vrxw', 'title': 'Musaddiq Ahmed 86 Score | KP vs Southern Punjab | QeA Trophy 2020-21 | PCB | MC2T', 'description': 'Musaddiq Ahmed 86 Score | KP vs Southern Punjab | QeA Trophy 2020-21 | PCB | MC2T Welcome to the official page of Pakistan Cricket Board. Get all your ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/mSF8ZHPCWjo/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/mSF8ZHPCWjo/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/mSF8ZHPCWjo/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Pakistan Cricket', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-08T13:37:19Z'}}, {'kind': 'youtube#searchResult', 'etag': 'nSTBOD_3shoP8nPczGG4AXYndYU', 'id': {'kind': 'youtube#video', 'videoId': 'nOwlfSDsG60'}, 'snippet': {'publishedAt': '2020-10-13T14:40:52Z', 'channelId': 'UCqqNSA3pIP1TLg8md15_qSw', 'title': '2020-10-13 - Premier League and International Cyber Cup Stream 2', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/nOwlfSDsG60/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/nOwlfSDsG60/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/nOwlfSDsG60/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'ESportsBattle Football', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-13T14:40:52Z'}}, {'kind': 'youtube#searchResult', 'etag': 'JLtffNXDEGRQPj72Qr2HblmcZ7k', 'id': {'kind': 'youtube#video', 'videoId': '7CdYDxZsggE'}, 'snippet': {'publishedAt': '2020-11-07T15:00:11Z', 'channelId': 'UCSUMyPPmunaDKk0YHxCK-cw', 'title': 'Game Of Aces - Full Action War Movie', 'description': 'Game Of Aces - Full Action War Movie An attempted rescue of a German traitor during World War I initiates an adventure across the desert. Release date: ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/7CdYDxZsggE/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/7CdYDxZsggE/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/7CdYDxZsggE/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Viewster', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-07T15:00:11Z'}}, {'kind': 'youtube#searchResult', 'etag': 'CneHL0tWsu8dqQQSQ3igiwGJycI', 'id': {'kind': 'youtube#video', 'videoId': '2s87j9mpLQU'}, 'snippet': {'publishedAt': '2020-10-12T11:18:52Z', 'channelId': 'UCEDTxryJDFBxsk5GeDSQ-Xg', 'title': 'Taxing Times and Blurry Lines', 'description': 'Karen invites Gizelle and Ashley to her homecoming in Virginia, but an emotional visit to her childhood farm shows the ladies a different side of the Grande ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/2s87j9mpLQU/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/2s87j9mpLQU/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/2s87j9mpLQU/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'The Real Housewives of Potomac', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-12T11:18:52Z'}}, {'kind': 'youtube#searchResult', 'etag': '7f30JgGmlYsFx4vzf_YJDNBtSa0', 'id': {'kind': 'youtube#video', 'videoId': 'qz5lqJ13C2M'}, 'snippet': {'publishedAt': '2020-10-16T04:02:06Z', 'channelId': 'UCBKmi9KVyY2y1VnXTyPazYw', 'title': 'Sister, Sister and a Babymoon', 'description': "Khloe takes her bestie on one last trip before her due date, but worries that some issues with Malika's baby daddy might send her friend into early labor.", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/qz5lqJ13C2M/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/qz5lqJ13C2M/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/qz5lqJ13C2M/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Keeping Up With the Kardashians', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-16T04:02:06Z'}}, {'kind': 'youtube#searchResult', 'etag': 'cGL2QkKH0-eHj2XFXCcSTRx1I_c', 'id': {'kind': 'youtube#video', 'videoId': 'o1wMKKDlaWY'}, 'snippet': {'publishedAt': '2020-10-16T07:00:01Z', 'channelId': 'UCC7QOlwrWzQyOlZ1zpjOSjg', 'title': 'Living It Up', 'description': 'A captivating romantic comedy about Lola (Hayek), a sexy waitress who meets Martin (Gomez), a charming millionaire. Their whirlwind romance screeches to a ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/o1wMKKDlaWY/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/o1wMKKDlaWY/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/o1wMKKDlaWY/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-16T07:00:01Z'}}, {'kind': 'youtube#searchResult', 'etag': '5QaI_gXfdmbScRX5QOwtmmYkvAM', 'id': {'kind': 'youtube#video', 'videoId': 'nzQ_SLtBf6I'}, 'snippet': {'publishedAt': '2020-11-09T13:13:25Z', 'channelId': 'UCCZVmatSqIMTTB8uExk8xEg', 'title': 'TEEKA TIWARI - &quot;COUNTDOWN CRYPTO&quot; - HOW EMBEDDED CODES IN CRYPTOCURRENCY PREDICT EXTRAORDINARY GAINS', 'description': 'The Crypto Catch-Up Event: https://londonreal.tv/crypto ✅ #BrianForMayor https://BrianForMayor.London BUILD YOUR DREAM BUSINESS IN 8 WEEKS: ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/nzQ_SLtBf6I/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/nzQ_SLtBf6I/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/nzQ_SLtBf6I/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'London Real', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-09T13:13:25Z'}}, {'kind': 'youtube#searchResult', 'etag': 'e39SmJ2BbB2rdu1IMYiP3U5p23E', 'id': {'kind': 'youtube#video', 'videoId': 'bA8hQ1ihDJM'}, 'snippet': {'publishedAt': '2020-11-04T08:00:06Z', 'channelId': 'UCC7QOlwrWzQyOlZ1zpjOSjg', 'title': 'Happy Christmas', 'description': 'When Jenny (Anna Kendrick), a hard-partying 20-something, moves in with her film director brother (Joe Swanberg), his wife Kelly (Melanie Lynskey), a budding ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/bA8hQ1ihDJM/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/bA8hQ1ihDJM/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/bA8hQ1ihDJM/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-04T08:00:06Z'}}, {'kind': 'youtube#searchResult', 'etag': 'UNyRkvrqpt9IUxIABfUlhsOoZVc', 'id': {'kind': 'youtube#video', 'videoId': 'PMjdWkOc4OI'}, 'snippet': {'publishedAt': '2020-11-08T10:00:05Z', 'channelId': 'UCk5AqT0PiOlMoMls5Src96A', 'title': 'PES 2021 | Valenvia vs Real Madrid | Penalty Shootout | Gameplay PC', 'description': 'Subscribe Please))) http://www.youtube.com/c/NiyazGamer.', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/PMjdWkOc4OI/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/PMjdWkOc4OI/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/PMjdWkOc4OI/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Niyaz Gamer', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-08T10:00:05Z'}}, {'kind': 'youtube#searchResult', 'etag': 'OA6IgH9RKkOrNQ8W1CDA4g3VGc8', 'id': {'kind': 'youtube#video', 'videoId': 'v9oQQkWqUGQ'}, 'snippet': {'publishedAt': '2020-11-01T07:00:06Z', 'channelId': 'UCC7QOlwrWzQyOlZ1zpjOSjg', 'title': 'Affliction', 'description': 'Based on the novel by Russell Banks, AFFLICTION is a sobering, absorbing psychological study of the precarious relationship between an abusive father and ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/v9oQQkWqUGQ/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/v9oQQkWqUGQ/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/v9oQQkWqUGQ/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'YouTube Movies', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-01T07:00:06Z'}}, {'kind': 'youtube#searchResult', 'etag': 'ctSztAN0RyStBN9_ACq7upasXF0', 'id': {'kind': 'youtube#video', 'videoId': '2TLOvk32Pt4'}, 'snippet': {'publishedAt': '2020-11-09T12:46:08Z', 'channelId': 'UCK-53mSZPJJdcbhD-vZcDAg', 'title': 'Cuchillo Damascus Simple Cook', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/2TLOvk32Pt4/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/2TLOvk32Pt4/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/2TLOvk32Pt4/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Kitchen Center', 'liveBroadcastContent': 'none', 'publishTime': '2020-11-09T12:46:08Z'}}]
>>>>>>> 851d1778427d899933d52117f34a18530a15b3f5
            ids = [n['id'] for n in json_response_items]
            video_ids = [id.get('videoId') for id in ids]
        return video_ids


    def get_search_snippets_between_dates_by_days_return_videoIds(self):
        json_response = RequestData.build_request(self.default_search_between_dates_by_days_return_videoIds_url)
        json_obj = json_response.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_response
        else:
            json_response_items = json_response['items']
            json_list = [val['id']['videoId'] for val in json_response_items]
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
        json_response = RequestData.build_request(self.default_video_statistics_by_videocategoryId_url)
        json_response_items = json_response["items"]
        json_obj = json_response.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_response
        else:
            for item in json_response_items:
                dic = {sub['id']: sub['statistics']['likeCount'] for sub in json_response_items}
        return dic


    def get_video_snippets_by_id(self):
        json_response = RequestData.build_request(self.default_video_snippets_by_id_url)
        json_response_items = json_response["items"]
        json_obj = json_response.keys()
        go_no_go = self.json_error_checker(json_obj)
        if go_no_go is True:
            return json_response
        else:
            json_response_id_snippet = {key["id"]:key["snippet"] for key in json_response_items}
        return json_response_id_snippet


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

        vid_ids = ','.join(new_vid_search_response)
        new_vid_snippet = Videos(id=vid_ids)
        #vid_snippet_response = new_vid_snippet.get_video_statistics_by_videocategoryId()
        vid_snippet_response = new_vid_snippet.get_video_snippets_by_id()
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

handler(None,None)
