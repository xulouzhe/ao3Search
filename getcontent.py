# -*- coding: utf-8 -*-
import requests
from lxml import etree
from items import articleItem
import re
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://archiveofourown.org/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
}


def GetArticle(name, page=1):
    url = "https://archiveofourown.org/works/search?page={0}utf8=%E2%9C%93&work_search%5Bquery%5D={1}".format(page, name)
    res = requests.get(url=url, headers=headers)
    res = etree.HTML(res.text)



    articles = res.xpath("//ol[@class='work index group']/li")
    # for x in articleLists:
    #     print(x.xpath("./div/h4/a/text()")) # 这里返回的是一个列表， 包含题目与作者两项
    #     print()
    articleList = []
    if not len(articles) == 0:
        for article in articles:
            article1 = articleItem()
            article1.title = article.xpath("./div/h4/a/text()")[0]
            article1.url = article.xpath("./div/h4/a/@href")[0]
            article1.author = article.xpath("./div/h4/a/text()")[1]
            article1.tag = article.xpath("./div/h5/a/text()")[0]
            article1.createTime = article.xpath("./div/p[@class='datetime']/text()")[0]

            articleList.append(article1)


    else:
        return None, None, 0
    pagenation = GetPagenation(res)
    number = GetArticleNumber(res)
    # print(number)
    return articleList, pagenation, number


def GetArticle(name, page=1):
    url = "https://archiveofourown.org/works/search?page={0}utf8=%E2%9C%93&work_search%5Bquery%5D={1}".format(page, name)
    res = requests.get(url=url, headers=headers)
    res = etree.HTML(res.text)



    articles = res.xpath("//ol[@class='work index group']/li")
    # for x in articleLists:
    #     print(x.xpath("./div/h4/a/text()")) # 这里返回的是一个列表， 包含题目与作者两项
    #     print()
    articleList = []
    if not len(articles) == 0:
        for article in articles:
            article1 = articleItem()
            article1.title = article.xpath("./div/h4/a/text()")[0]
            article1.url = article.xpath("./div/h4/a/@href")[0]
            article1.author = article.xpath("./div/h4/a/text()")[1]
            article1.tag = article.xpath("./div/h5/a/text()")[0]
            article1.createTime = article.xpath("./div/p[@class='datetime']/text()")[0]
            try:
                article1.summary = article.xpath("./blockquote[contains(@class, 'summary')]/p/text()")[0]
            except:
                pass
            articleList.append(article1)

    else:
        return None, None, 0
    try:
        pagenation = GetPagenation(res)
    except:
        pagenation = False
    number = GetArticleNumber(res)
    # print(number)
    return articleList, pagenation, number

def GetArticleNumber(res):
    number = res.xpath('//h3[@class="heading"]/text()')[0]
    number = re.sub(r'/s', '', number)
    number = re.sub(r'[a-zA-Z]', '', number)
    return number

def GetPagenation(res):
    pagenation = res.xpath("//ol[@class='pagination actions']")[0]
    print(etree.tostring(pagenation).decode("utf-8"))
    return ParsePagenation(etree.tostring(pagenation).decode("utf-8"))

def ParsePagenation(pagenation):
    pagenation2 = re.sub(r'<li class="gap">&#8230;</li>', '<li class="disabled"><a href="">&#8230;</a></li>', pagenation)
    pagenation2 = re.sub(r'<li><span class="current">(\d+?)</span></li>',
                         r'<li class="active"><a href="#">\1 <span class="sr-only">(current)</span></a></li>',
                         pagenation2)
    pagenation2 = re.sub(r'<li class="previous" title="previous"><span class="disabled">&#8592; Previous</span></li>',
                         r'<li class="disabled"><a href="" aria-label="Previous"><span aria-hidden="true">&#8592; Previous</span></a></li>',
                         pagenation2)
    pagenation2 = re.sub(r'<li class="next" title="next"><span class="disabled">Next &#8594;</span></li>',
                         r'<li class="disabled"><a href="" aria-label="Next"><span aria-hidden="true">Next &#8594;</span></a></li>',
                         pagenation2)
    return pagenation2

if __name__ == '__main__':
    articleList = GetArticle("下坠")
    # print(articleList[11].tag)

    # print("下坠".encode("utf-8").de)

