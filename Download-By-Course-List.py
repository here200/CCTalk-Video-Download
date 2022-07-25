import requests
import jsonpath
import json


class CCTalk(object):

    def __init__(self, series_id):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            # 有些视频需要购买才能观看，登录CCTalk后，把cookies复制到这里
            # 解除权限的限制
            "cookie": ""
        }
        self.series_id = series_id

    def get_data(self, url, params=None):
        response = requests.get(url, headers=self.headers, params=params)
        return response.content

    # 获取课程中每个视频的id
    def get_movie_id(self, series_id):
        # url
        url = 'https://www.cctalk.com/webapi/content/v1.2/series/all_lesson_list'
        # params
        params = {
            'seriesId': series_id
        }
        # 发送请求,获取数据
        tmp = self.get_data(url, params=params).decode()
        # 解析数据，获取每个视频的id号
        course_list = json.loads(tmp)
        movie_list = jsonpath.jsonpath(course_list, '$..items..contentId')
        return movie_list

    # 获取每个视频的标题和链接，并将信息放到movie_list中
    def get_movie_title_links(self, movie_id, movie_list):
        # params
        params = {
            'videoId': str(movie_id)
        }
        # url
        url = 'https://www.cctalk.com/webapi/content/v1.1/video/detail'
        # 发送数据
        tmp = self.get_data(url, params=params).decode()
        # 解析数据，获取视频标题和链接
        movie = json.loads(tmp)
        title = jsonpath.jsonpath(movie, '$..videoName')[0] + '.mp4'
        movie_href = jsonpath.jsonpath(movie, '$..videoUrl')[0]
        # 创建视频信息，并追加到视频列表中
        data = {
            'index': len(movie_list),
            'name': title,
            'url': movie_href
        }
        movie_list.append(data)

    def download_movie(self, movie_list, index):
        # 获取视频链接
        href = movie_list[index]['url']
        # 发送请求，获取视频
        response = requests.get(href)
        # 保存视频
        with open('./data/' + movie_list[index]['name'], 'wb') as f:
            f.write(response.content)

    def run(self):
        # 获取课程中每个视频的id
        movie_id = self.get_movie_id(self.series_id)
        # 创建视频列表
        movie_list = []
        for e in movie_id:
            # 获取每个视频的标题和链接
            self.get_movie_title_links(e, movie_list)
        # 打印视频列表信息
        for e in movie_list:
            print(e)
        # 下载选中的视频
        # self.download_movie(movie_list, 32)


if __name__ == '__main__':
    cctalk = CCTalk('1612582780690810')
    cctalk.run()
