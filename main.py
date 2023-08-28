from typing import Any
from os import PathLike

import json

import googleapiclient.discovery
from google.oauth2 import service_account

from modules.DataPullModule import DataPullModule
from modules.DataSaveModule import DataSaveModule

from objects.PaginatedResults import PaginatedResults
from objects.Channel import Channel

class YoutubeDataScraper(object):

    YOUTUBE_CLIENT : Any # They literally don't tell me the type

    DATA_PULL_MODULE : DataPullModule
    DATA_SAVE_MODULE : DataSaveModule

    def build_youtube_client(self) -> Any:

        # Create a credentials instance from the credentials json file
        c = service_account.Credentials.from_service_account_file(
            "./creds.json"
        )

        # Build the client and return it
        return googleapiclient.discovery.build(
            serviceName="youtube",
            version="v3",
            credentials = c
        )
        

    def __init__(self) -> None:

        # Build our youtube client using our credentials file
        self.YOUTUBE_CLIENT = self.build_youtube_client()

        # Instantiating the module that pulls the data
        self.DATA_PULL_MODULE = DataPullModule(yt=self.YOUTUBE_CLIENT)
        self.DATA_SAVE_MODULE = DataSaveModule()

    def pull_channel_data_from_json_list(self, fp : PathLike = './channel_list.json'):
        
        with open(fp, 'r') as jsF:
            channels_to_read = json.load(jsF)
        
        for i, c in enumerate(channels_to_read, start=1):
            print("Pulling data for channel: %s (%d/%d)" % (c, i, len(channels_to_read)))
            self.channel_data_pull_loop(c)

        print("Done!")

    def channel_data_pull_loop(self, channel_handle : str) -> None:

        # First, fetch the channel id from YouTube, as you cannot directly pull channel data without it
        channel_id = self.DATA_PULL_MODULE.fetch_channel_id_from_handle(channel_handle)

        # Create a `Channel` instance, from the data pulled with the `channel_id`
        channel : "Channel" = self.DATA_PULL_MODULE.fetch_channel_from_id(channel_id)

        # Save the Channel data to create the initial file for all the information we need
        self.DATA_SAVE_MODULE.save_channel_data(channel)

        # Create an instance of PaginatedResults to grab video ids from the channel's upload playlist
        playlistPagination : "PaginatedResults" = self.DATA_PULL_MODULE.fetch_videos_from_playlist(channel.uploads_playlist)

        # If there is no video data from the playlist, (usually in the event of a channel having no videos) ...
        # do nothing. 
        if playlistPagination is None:
            return

        while True:

            # Request all of the videos given by the last call to the playlist lookup endpoint
            videos = self.DATA_PULL_MODULE.fetch_videos_from_id_array(playlistPagination.map_to_response(lambda n: n.video_id))

            # Save the video data we got
            self.DATA_SAVE_MODULE.save_video_data_for_channel(channel, videos)

            # Detect if there's another page, if there is, then go through and repeat this whole loop again
            if playlistPagination.hasNextPage():
                playlistPagination.next()

            # Otherwise, we break the loop if we hit the end of the results. 
            else:
                break



if __name__ == "__main__":

    yt = YoutubeDataScraper()
    yt.pull_channel_data_from_json_list(
        './channel_list.json'
    )
        