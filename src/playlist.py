import os, datetime, isodate

from googleapiclient.discovery import build


class PlayList:
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    """
    Класс для плейлиста
    """
    def __init__(self, playlist_id: str) -> None:
        """
        Экземпляр инициализируется id плейлиста
        """
        self.playlist = self.youtube.playlists().list(part="snippet,contentDetails", id=playlist_id).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(
            playlistId=playlist_id,
            part='contentDetails',
            maxResults=50,
        ).execute()
        self.video_id: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=','.join(self.video_id)
                                                         ).execute()
    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        """
        total_duration_time = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration_time += duration
        return total_duration_time

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        like_count = 0
        for video in self.video_response['items']:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video['id']).execute()
            if int(video_response['items'][0]['statistics']['likeCount']) > like_count:
                like_count = int(video_response['items'][0]['statistics']['likeCount'])
                self.url = video_response['items'][0]['id']

        return f'https://youtu.be/{self.url}'
