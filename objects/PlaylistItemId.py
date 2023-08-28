from dataclasses import dataclass

@dataclass
class PlaylistItemId(object):
    video_id : str

    @classmethod
    def construct_from_response(cls, resp : dict) -> "PlaylistItemId":
        
        return cls( video_id = resp['snippet']['resourceId']['videoId'] )