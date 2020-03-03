import requests
from lxml import etree
from items import articleItem
import re


def GetArticle(name, page=None):
    if page is None:
        url = "https://archiveofourown.org/works/search?utf8=%E2%9C%93&work_search%5Bquery%5D={}".format(name)
    else:
        url = "https://archiveofourown.org/works/search?page={0}utf8=%E2%9C%93&work_search%5Bquery%5D={1}".format(page, name)
    res = requests.get(url=url)
    res = etree.HTML(res.text)
    pagenation = GetPagenation(res)
    articles = res.xpath("//ol[@class='work index group']/li")
    # for x in articleLists:
    #     print(x.xpath("./div/h4/a/text()")) # 这里返回的是一个列表， 包含题目与作者两项
    #     print()
    articleList = []
    for article in articles:
        article1 = articleItem()
        article1.title = article.xpath("./div/h4/a/text()")[0]
        article1.author = article.xpath("./div/h4/a/text()")[1]
        article1.tag = article.xpath("./div/h5/a/text()")[0]
        article1.createTime = article.xpath("./div/p[@class='datetime']/text()")[0]
        articleList.append(article1)
    return articleList, pagenation


def GetPagenation(res):
    pagenation = res.xpath("//ol[@class='pagination actions']")[0]
    print(etree.tostring(pagenation).decode("utf-8"))
    return ParsePagenation(etree.tostring(pagenation).decode("utf-8"))

def ParsePagenation(pagenation, page=None):
    pagenation2 = re.sub(r'<li class="gap">&#8230;</li>', '<li class="disabled"><a href="">&#8230;</a></li>', pagenation)
    pagenation2 = re.sub(r'<li><span class="current">1</span></li> <li><a rel="next" href="/works/search?page=2&amp;view_adult=true&amp;work_search%5Bquery%5D=">2</a></li>',
                         '<li class="disabled"><a href="">&#8230;</a></li>',
                         pagenation)
    pagenation2 = re.sub(r'<li class="previous" title="previous"><span class="disabled">&#8592; Previous</span></li>',
                         '<li class="disabled"><a href="" aria-label="Previous"><span aria-hidden="true">&#8592; Previous</span></a></li>',
                         pagenation2)
    return pagenation2

if __name__ == '__main__':
    articleList = GetArticle("下坠")
    # print(articleList[11].tag)

    # print("下坠".encode("utf-8").de)

