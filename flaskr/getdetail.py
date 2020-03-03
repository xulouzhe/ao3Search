import requests
from lxml import etree
from items import articleDetailItem
import re


def GetDetail(id):
    url = "https://archiveofourown.org/works/{}".format(id)
    res = requests.get(url)
    html = etree.HTML(res.text)
    contents = html.xpath('//div[contains(@class, "userstuff")]/p/text()')
    # for x in contents:
    #     x = re.sub(r"\s", "", x)
    content = "<br /><br />".join(contents)
    content = re.sub(r"\s", "", content)
    wrapper = [re.sub(r"<.+?>", " ", etree.tostring(x).decode("utf-8")) for x in html.xpath('//dl[@class="work meta group"]/*')]
    newWrapper = [(x +' '+ y) for (x, y) in zip(wrapper[0::2], wrapper[1::2])]
    # print(content)
    articleDetail = articleDetailItem()
    articleDetail.content = content
    articleDetail.wrapper = newWrapper
    return articleDetail



if __name__ == '__main__':
    GetDetail(22478632)