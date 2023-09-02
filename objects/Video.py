from datetime import datetime
from typing import (
    List, Union
)
from dataclasses import dataclass, asdict

@dataclass
class Video(object):

    video_id : str
    published_at : str
    channel_id : str
    title : str
    description : str
    channel_title : str
    video_tags : List[str]
    video_title_language : str
    video_audio_language : str
    video_length : str
    video_dimension : str
    video_definition : str
    video_captions : bool
    video_content_licensing : bool
    video_region_restrictions : dict
    video_ratings : dict                 # REQUIRES SEPERATE RATINGS: TVPG, YTRATING
    license : str
    embeddable : str
    viewable_stats : bool
    for_kids : bool
    view_count : int
    like_count : int
    comment_count : int
    video_topics : List[str]
    recording_date : Union[str, None] 
    live_start_time : Union[str, None]
    live_end_time : Union[str, None]
    live_scheduled_start : Union[str, None]
    live_scheduled_end : Union[str, None]

    is_age_restricted : bool
    tvpg_rating : str

    @classmethod
    def construct_from_response(cls, response : dict) -> "Video":

        if 'commentCount' not in response['statistics'].keys():
            print(response['statistics'], response['id'])

        return cls(
            video_id = response['id'],
            published_at = response['snippet']['publishedAt'],
            channel_id = response['snippet']['channelId'],
            title = response['snippet']['title'],
            description = response['snippet']['description'],
            channel_title = response['snippet']['channelTitle'],
            video_tags = response['snippet'].get('tags', []),
            video_title_language = response['snippet'].get('defaultLanguage', None),
            video_audio_language = response['snippet'].get('defaultAudioLanguage', None),
            video_length = response['contentDetails']['duration'],
            video_dimension = response['contentDetails']['dimension'],
            video_definition = response['contentDetails']['definition'],
            video_captions = response['contentDetails']['caption'] == 'true',
            video_content_licensing = response['contentDetails']['licensedContent'],
            video_region_restrictions = response['contentDetails'].get('regionRestriction', {"allowed" : [], 'blocked' : []}),
            video_ratings = response['contentDetails']['contentRating'],
            license = response['status']['license'],
            embeddable = response['status']['embeddable'],
            viewable_stats = response['status']['publicStatsViewable'],
            for_kids = response['status']['madeForKids'],
            view_count = response['statistics']['viewCount'],
            like_count = response['statistics'].get('likeCount', -1),       # -1 --> Likes are hidden
            comment_count = response['statistics'].get('commentCount', -1), # -1 --> Comments are hidden
            video_topics = response.get('topicDetails', {}).get('topicCategories', []),
            recording_date = response['recordingDetails'].get("recordingDate", None),
            live_start_time = response.get('liveStreamingDetails', {}).get('actualStartTime', None),
            live_end_time = response.get('liveStreamingDetails', {}).get('actualEndTime', None),
            live_scheduled_start = response.get('liveStreamingDetails', {}).get('scheduledStartTime', None),
            live_scheduled_end = response.get('liveStreamingDetails', {}).get('scheduledEndTime', None),
            is_age_restricted = response['contentDetails']['contentRating'].get('ytRating', 0) == 'ytAgeRestricted',
            tvpg_rating = response['contentDetails']['contentRating'].get('tvpgRating', 'tvpgUnrated')
        )
    
    def to_json(self):
        return asdict(self)