from datetime import datetime
from typing import ( List, Union )
from dataclasses import dataclass, asdict

@dataclass
class Channel(object):

    channel_id : str
    title : str
    description : str
    created_at : str
    liked_video_playlist : int
    uploads_playlist : str # The id of the playlist which contains all the channel's uploaded videos
    total_views : int
    total_subscribers : int
    hidden_subcount : bool
    video_count : int
    channel_categories : List[str]
    channel_privacy : str
    made_for_kids : bool
    moderated_comments : bool
    default_language : Union[str, None]

    handle : str # We use this for file names and whatnot

    @classmethod
    def construct_from_response(cls, response : dict) -> "Channel":

        x = cls(
            channel_id = response['id'],
            title = response['snippet']['title'],
            description=response['snippet']['description'],
            created_at = response['snippet']['publishedAt'],
            liked_video_playlist = response['contentDetails']['relatedPlaylists']['likes'] if response['contentDetails']['relatedPlaylists']['likes'] != "" else None,
            uploads_playlist = response['contentDetails']['relatedPlaylists']['uploads'],
            total_views = response['statistics']['viewCount'],
            total_subscribers = response['statistics']['subscriberCount'],
            hidden_subcount = response['statistics']['hiddenSubscriberCount'],
            video_count = response['statistics']['videoCount'],
            channel_categories = response.get('topicDetails', {}).get('topicCategories', []),
            channel_privacy = response['status']['privacyStatus'],
            made_for_kids = response['status'].get('madeForKids', None), # Smaller Channels sometimes do not set this option, and it isn't given to us.
            moderated_comments =  response['brandingSettings']['channel'].get('moderateComments', False),
            default_language = response['brandingSettings']['channel'].get('defaultLanguage', None),
            handle = response['snippet']['customUrl'].replace('@', '')
        )
        
        return x
    
    def to_json(self):
        return asdict(self)