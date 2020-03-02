import requests
from lxml import etree


def GetArticle(name):
    res = requests.get("https://archiveofourown.org/works/search?utf8=%E2%9C%93&work_search%5Bquery%5D={}".format(name))
    res = etree.HTML(res.text)

    articleList = res.xpath("//ol[@class='work index group']/li")
    # for x in articleLists:
    #     print(x.xpath("./div/h4/a/text()")) # 这里返回的是一个列表， 包含题目与作者两项
    #     print()
    return articleList


if __name__ == '__main__':
    articleList = GetArticle("下坠")
    for article in articleList:
        article = {}
        article["title"] = article.xpath("./div/h4/a/text()")[0]
        article["author"] = article.xpath("./div/h4/a/text()")[0]
        print
    # print("下坠".encode("utf-8").de)

