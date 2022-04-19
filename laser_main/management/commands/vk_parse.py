import time
from datetime import datetime

import requests
import json
from laser_main.models import Post
from django.core.management.base import BaseCommand
from django.utils.safestring import mark_safe
from config import vk_token as vk

# список с поставми которые уже есть
all_posts = []


class VkParser():

    def parse_all(self):
        vk_token = vk
        api = f'https://api.vk.com/method/wall.get?owner_id=-166417195&access_token={vk_token}&v=5.131&count=20'
        req = json.loads(requests.get(api).text)
        posts_list = req['response']['items']
        posts = Post.objects.all()
        for p in posts:
            all_posts.append(p.post_id)
        for post in posts_list:
            if not post.get('is_pinned') and post['id'] not in all_posts:
                file = post['attachments'][0]
                date = datetime.utcfromtimestamp(int(post['date'])).strftime('%Y-%m-%d')
                if file['type'] == 'photo':
                    url = file['photo']['sizes'][-1]['url']
                    req_photo = requests.get(url)
                    with open(f"media/{post['id']}.jpg", "wb") as file:
                        file.write(req_photo.content)
                    file_name = f"{post['id']}.jpg"
                    p = Post(
                        post_id=post['id'],
                        text=mark_safe(post['text'].replace("\n", "<br/>").replace("[club166417195|Laser Zone]",
                                                                                   "<a href='https://vk.com/laserzone'>Laser Zone</a>").replace(
                            "[id487396752|Anna Laser-Zone]",
                            "<a href='https://vk.com/annalaserzone'>Anna Laser-Zone</a>").replace(
                            "https://n122053.yclients.com/",
                            "<a href='https://n122053.yclients.com/'>https://n122053.yclients.com/</a>")),
                        data=date,
                        photo=file_name
                    ).save()

                elif file['type'] == 'video':
                    video_id = file['video']['id']
                    video_url_api = f'https://api.vk.com/method/video.get?owner_id=-166417195&access_token={vk_token}&v=5.131&videos=-166417195_{video_id}'
                    req_video_api = json.loads(requests.get(video_url_api).text)
                    video_url = req_video_api['response']['items'][0]['player']
                    p = Post(
                        post_id=post['id'],
                        text=mark_safe(post['text'].replace("\n", "<br/>").replace("[club166417195|Laser Zone]",
                                                                                   "<a href='https://vk.com/laserzone'>Laser Zone</a>").replace(
                            "[id487396752|Anna Laser-Zone]",
                            "<a href='https://vk.com/annalaserzone'>Anna Laser-Zone</a>").replace(
                            "https://n122053.yclients.com/",
                            "<a href='https://n122053.yclients.com/'>https://n122053.yclients.com/</a>")),
                        data=date,
                        video=video_url
                    ).save()

        print('done')


class Command(BaseCommand):
    help = "Parse vk"

    def handle(self, *args, **options):
        while True:
            p = VkParser()
            p.parse_all()
            time.sleep(60)
