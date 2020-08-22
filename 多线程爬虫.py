import requests
from lxml import etree
import os
from concurrent.futures import ThreadPoolExecutor

try:
    if not os.path.exists("boss"):
        os.mkdir("boss")
except:
    pass
print(os.path.abspath(__name__))
worker = ThreadPoolExecutor(40)  # 创建4个线程


# 高端 0.7
# 版本二
def get_img(img_url, title, end_str):
    img_content = requests.get(url=img_url).content
    with open(f"boss/{title}.{end_str}", "wb") as fp:
        fp.write(img_content)
        print(f"已经成功爬取{title}的图片")


def run(img_url_dict):
    for img_dict in img_url_dict:
        img_url = img_dict["img_url"]
        title = img_dict["title"]
        end_str = img_dict["end_str"]
        worker.submit(get_img, img_url, title, end_str)


def get_img_url(url):  # 执行 开始爬取
    html = requests.get(url=url)
    html.encoding = "gbk"
    soup = etree.HTML(html.text)
    li_list = soup.xpath('//div[@class="bossul_n"]/ul/li')
    img_list = []
    for li in li_list:
        img_url_list = {}  # type:dict
        img_url_list["img_url"] = li.xpath('a/img/@src')[0]
        img_url_list["title"] = li.xpath('a/text()')[0]
        img_url_list["end_str"] = li.xpath('a/img/@src')[0].split('.')[-1]
        img_list.append(img_url_list)
    run(img_list)


def main():  # 把每个url分别给了一个线程
    url_list = [f"http://news.4399.com/gonglue/zmxy3/boss/4413-{i}.html" for i in range(1, 5)]  # 生成4个页得url
    for url in url_list:
        get_img_url(url)


if __name__ == '__main__':
    main()
