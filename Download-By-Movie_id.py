import requests
import jsonpath
import json

def download_by_movie_id(id):
    # url
    url = 'https://www.cctalk.com/webapi/content/v1.1/video/detail'
    # headers
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        # 如果视频需要登录才能下载，请携带你的cookies
        "cookie": ""
    }
    # params
    params = {
        'videoId': id
    }
    # 发送请求
    response = requests.get(url, headers=headers, params=params)
    # 解析数据，获取视频标题和链接
    movie = json.loads(response.content.decode())
    title = jsonpath.jsonpath(movie, '$..videoName')[0] + '.mp4'
    movie_href = jsonpath.jsonpath(movie, '$..videoUrl')[0]
    # 打印视频信息
    print('title:', title, ' href:', movie_href)
    # 发送请求，把视频数据拿到
    movie_file = requests.get(movie_href, headers=headers)
    # 保存到文件中
    with open('./data/' + title, 'wb') as f:
        f.write(movie_file.content)

if __name__ == '__main__':
    # 从输入的链接中提取id
    id = '16415221843564'
    download_by_movie_id(id)
