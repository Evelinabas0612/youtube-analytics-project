import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    print(api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https:////www.youtube.com//channel//' + self.channel['items'][0]['id']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(channel)

    @classmethod
    def get_service(cls):
        """
        класс-метод возвращает объект для работы с YouTube API
        """
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file):
        """
        Сохраняет в файл значения атрибутов
        """
        dict_channel = {
            'id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriberCount': self.subscriber_count,
            'video_count': self.video_count,
            'viewCount': self.view_count
        }
        with open(file, 'w', encoding='utf-8') as file:
            json.dump(dict_channel, file, ensure_ascii=False)

    def __str__(self):
        """
        Возвращает название и ссылку на канал по шаблону <название_канала> (<ссылка_на_канал>)
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """
        Реалузет возможность складывать два канала между собой.
        """
        return int(self.subscriber_count) + int(other.subscriber_count)


    def __sub__(self, other):
        """
        Реалузует возможность вычитать два канала между собой.
        """
        return int(self.subscriber_count) - int(other.subscriber_count)

    # def __gt__(self, other):
    #     """
    #     Реалузует возможность сравнивать два канала между собой ("больше").
    #     """
    #     return self.subscriber_count > other.subscriber_count
    #
    # def __ge__(self, other):
    #     """
    #     Реалузует возможность  сравнивать два канала между собой ("больше или равно").
    #     """
    #     return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """
        Реалузует возможность сравнивать два канала между собой ("меньше").
        """
        return self.subscriber_count > other.subscriber_count

    def __le__(self, other):
        """
        Реалузует возможность  сравнивать два канала между собой ("меньше или равно").
        """
        return self.subscriber_count >= other.subscriber_count

    def __eq__(self, other):
        """
        Реалузует возможность  сравнивать два канала между собой("равно").
        """
        return self.subscriber_count == other.subscriber_count
