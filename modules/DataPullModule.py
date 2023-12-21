from typing import (
    Any, Union, List
)

from objects.Channel import Channel
from objects.PaginatedResults import PaginatedResults
from objects.Video import Video
from objects.PlaylistItemId import PlaylistItemId

from googleapiclient.errors import HttpError

class DataPullModule(object):

    YOUTUBE_CLIENT : Any

    def __init__(self, yt) -> None:
        self.YOUTUBE_CLIENT = yt

    def grab_channel_id_from_string(self, s : str) -> Union[str, None]:
        if s.startswith('/c/'):
            return s[3:]
        else:
            return self.fetch_channel_id_from_handle(s)

    def fetch_channel_id_from_handle(self, handle : str) -> Union[str, None]:

        req = self.YOUTUBE_CLIENT.search().list(
            part = "id",
            maxResults=1,
            q = handle if handle.startswith("@") else ("@" + handle),
            type = "channel"
        )

        res = req.execute()

        # Return none if no results are found for the channel
        if len(res.get("items", [])) < 1:
            return None
                
        # A really poorly thought out way to get the channel id
        return res.get('items', [])[0].get("id", {}).get("channelId")
    


    def fetch_channel_from_id(self, _id : str) -> Channel:

        req = self.YOUTUBE_CLIENT.channels().list(
            part="snippet,contentDetails,statistics,topicDetails,status,brandingSettings",
            id = _id
        )

        res = req.execute()

        return Channel.construct_from_response(res['items'][0])
    


    def fetch_videos_from_playlist(self, playlist_id : str) -> Union[PaginatedResults, None]:

        req = self.YOUTUBE_CLIENT.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId=playlist_id
        )

        try:
            res = req.execute()

        except HttpError as err:
            
            if err.error_details[0]['reason'] == 'playlistNotFound':
                return None

        return PaginatedResults(
            self.YOUTUBE_CLIENT,
            req, 
            res,
            self.YOUTUBE_CLIENT.playlistItems(),
            PlaylistItemId
        )



    def fetch_videos_from_id_array(self, ids : List[PlaylistItemId]) -> PaginatedResults:
        
        req = self.YOUTUBE_CLIENT.videos().list(
            part="id,snippet,contentDetails,statistics,status,topicDetails,recordingDetails,liveStreamingDetails",
            id = ','.join(ids)
        )

        res = req.execute()

        return PaginatedResults(
            self.YOUTUBE_CLIENT,
            req, res,
            self.YOUTUBE_CLIENT.videos(),
            Video
        )