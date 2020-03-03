import requests
from lxml import etree
from items import articleDetailItem
import re
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'accepted_tos=20180523; _otwarchive_session=TFFzdGJVaGdGTHRzd3FDRHZPRExiaTRRREZ1NEVYKzRmVEdWb2czQURsV2JMcWdmZkNWbllvQUpGSXNCRUdxTENldytYeW5rMWxBK2l3V3MyWG1xOHBCYUpTWVd0djdUN3E2OW9WSUtONUVla29YdlhWcjRpc3Q1TEFJS2NzNDhMbXRERml5VURRUTc2K29pTVRqdCtSVzJFTlRUTjFxS0ZQcUl6VVk5Q2dXNXhxb051MVJEdHhPQXhaeW1zS1QwTWh1RlRrSnMxdklNM1JpYU9DdTgzTHhlM1BXdkJCSGI2RlFqdDh2T1NNMU1hcDBLUS9odi9LaHUyQm01bURoTy9ndmlybDROeVN1ZFYvSnorNjVXVlE9PS0tNS9KVFQzS1NsRjI1bUhnTWxWNVNOdz09--adb18f449972f0cebdd0f8715a7115f94e86c565',
    'referer': 'https://archiveofourown.org/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
}

def GetDetail(id):
    url = "https://archiveofourown.org/works/{}?view_adult=true".format(id)
    try:
        res = requests.get(url=url, headers=headers)

        print(res)
        print(res.text)
        html = etree.HTML(res.text)
        contents = html.xpath('//div[contains(@class, "userstuff")]/p/text()')
        # for x in contents:
        #     x = re.sub(r"\s", "", x)
        content = "<br /><br />".join(contents)
        content = re.sub(r"\s", "", content)
        wrapper = [re.sub(r"<.+?>", " ", etree.tostring(x).decode("utf-8")) for x in html.xpath('//dl[@class="work meta group"]/*')]
        newWrapper = [(x + ' ' + y) for (x, y) in zip(wrapper[0::2], wrapper[1::2])]
        # print(content)
        articleDetail = articleDetailItem()
        articleDetail.author = str(html.xpath('//h3[@class="byline heading"]/a/text()')[0])
        articleDetail.title = str(html.xpath('//h2[@class="title heading"]/text()')[0])
        try:
            articleDetail.chapterTitle = str(html.xpath('//h3[@class="title"]/a/text()')[0])
        except:
            articleDetail.chapterTitle=""
        # if articleDetail.title is None:
        #     articleDetail.title = ""
        articleDetail.content = content
        articleDetail.wrapper = newWrapper
        articleDetail.url = url
        return articleDetail


    except requests.exceptions.ConnectionError:
        print("请求错误", url)
        return None


if __name__ == '__main__':
    GetDetail(22478632)