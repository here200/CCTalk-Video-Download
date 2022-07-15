import requests
import jsonpath
import json


class Cctalk(object):
    def __init__(self):
        # headers
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            # 如果视频需要登录才能下载，请携带你的cookies
            "cookie": ""
        }

    def search_by_movie_id(self, id):
        # url
        url = 'https://www.cctalk.com/webapi/content/v1.1/video/detail'
        # params
        params = {
            'videoId': id
        }
        # 发送请求
        content = requests.get(url, headers=self.headers, params=params)
        # 解析数据，获取视频标题和链接
        movie = json.loads(content.content.decode())
        title = jsonpath.jsonpath(movie, '$..videoName')[0] + '.mp4'
        movie_href = jsonpath.jsonpath(movie, '$..videoUrl')[0]
        # 保存视频信息
        movie_list = {"name": title, "url": movie_href}
        # 打印视频信息
        print(movie_list)
        return movie_list

    def save_movie(self, movie_list):
        # 发送请求，把视频数据拿到
        movie_file = requests.get(movie_list['url'], headers=self.headers)
        # 保存到文件中
        with open('./data/' + movie_list['name'], 'wb') as f:
            f.write(movie_file.content)


if __name__ == '__main__':
    # 创建一个Cctalk对象
    ccTalk = Cctalk()
    # 通过视频id来搜索视频
    movie_list = ccTalk.search_by_movie_id('16444799633133')
    # 下载视频
    # ccTalk.save_movie(movie_list)
