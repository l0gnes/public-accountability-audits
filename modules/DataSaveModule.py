from objects.Channel import Channel
from objects.Video import Video
from objects.PaginatedResults import PaginatedResults

from typing import (
    Literal, List
)
from os import PathLike
import os.path
import json



class ChannelFSFailure(Exception):
    pass

class InvalidVideoWrapperClass(Exception):
    pass



class DataSaveModule(object):

    out_path : PathLike = "./data/"

    """
    Json Output will have an indent of 4 if this option is set to True.
    Only really useful when debugging code. Encouraged to be turned of in production
    """
    prettify_output : bool = True

    """
    Overwrite Behavior: Determines what should happen in the event of filepath
    issues. 
        'skip' -> Skip the file and silently move onto the next one
        'overwrite' -> Delete the progress made on the current file, and write the new data. 
    """
    overwrite_behaviour : Literal["skip", "overwrite"] = 'overwrite'


    def ensure_out_exists(self) -> None:
        
        if not os.path.exists(self.out_path):
            os.makedirs(self.out_path)

    def fs_ensure_free_channel_path(self, channel : Channel, *, overwrite : bool = True) -> bool:
        
        self.ensure_out_exists()

        p = os.path.join(self.out_path, "%s.json" % channel.handle.lower())

        if os.path.exists( p ):

            if not overwrite:
                return True

            if self.overwrite_behaviour == 'overwrite':
                os.remove(p)

            elif self.overwrite_behaviour == 'skip':
                raise ChannelFSFailure

            else: # In case of a typo, I don't want the program to default to removing files.
                raise ChannelFSFailure

        return True
            

    def get_proposed_channel_path(self, channel : Channel, *, overwrite : bool = True) -> PathLike:
        self.fs_ensure_free_channel_path(channel, overwrite=overwrite)
        p = os.path.join(self.out_path, "%s.json" % channel.handle.lower())
        return p


            
    def save_channel_data(self, channel : Channel) -> None:
        
        fp = self.get_proposed_channel_path(channel)

        x = channel.to_json()

        # Prepare for video data
        x['VIDEO_DATA'] = []

        with open(fp, "w+") as jsF:
            json.dump(x, jsF, indent= None if not self.prettify_output else 4)



    def save_video_data_for_channel(self, channel : Channel, videos : PaginatedResults) -> None:

        if videos.WRAPPER_CLASS != Video:
            raise InvalidVideoWrapperClass

        fp = self.get_proposed_channel_path(channel, overwrite=False)

        with open(fp, 'r') as jsF:
            current_channel_data = json.load(jsF)

        current_channel_data['VIDEO_DATA'].extend(
            videos.map_to_response(lambda n: n.to_json())
        )

        with open(fp, 'w+') as jsF:
            json.dump(current_channel_data, jsF, indent= None if not self.prettify_output else 4)