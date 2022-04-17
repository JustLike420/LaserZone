import requests
import json
from laser_main.models import Post
from django.core.management.base import BaseCommand
from django.utils.safestring import mark_safe

# список с поставми которые уже есть
all_posts = [616]


class VkParser():

    def parse_all(self):
        vk_token = '8a1ce177eb4e27ae374e7cfd6161bc5243f876fb626b19eb80cf4e3cb99e59eef2646b3a80628d75c2915'
        api = f'https://api.vk.com/method/wall.get?owner_id=-166417195&access_token={vk_token}&v=5.131&count=5'
        req = json.loads(requests.get(api).text)
        posts_list = req['response']['items']
        for post in posts_list:
            if post['id'] not in all_posts:
                text = post['text']
                date = post['date']
                p = Post(
                    post_id=post['id'],
                    text=mark_safe(post['text'].replace("\n", "<br/>").replace("[club166417195|Laser Zone]",
                                                                               "<a href='https://vk.com/laserzone'>Laser Zone</a>").replace(
                        "[id487396752|Anna Laser-Zone]",
                        "<a href='https://vk.com/annalaserzone'>Anna Laser-Zone</a>").replace(
                        "https://n122053.yclients.com/", "<a href='https://n122053.yclients.com/'>https://n122053.yclients.com/</a>")),
                    data='2022-04-16',
                ).save()
                print(p)


class Command(BaseCommand):
    help = "Parse vk"

    def handle(self, *args, **options):
        p = VkParser()
        p.parse_all()
