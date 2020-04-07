# -*- coding: utf-8 -*-
import requests
from lxml import etree
from items import articleDetailItem
import re
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,\
    */*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://archiveofourown.org/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/80.0.3987.122 Safari/537.36',
}


def GetDetail(id, chapter=None, full=None):
    if chapter is None:
        url = "https://archiveofourown.org/works/{}?view_adult=true".format(id)
        if not full is None:
            url = url + "&view_full_work=true"
            print(url)
    else:
        url = "https://archiveofourown.org/works/{}/chapters/{}?view_adult=true".format(id, chapter)
        print(url)
    res = requests.get(url=url, headers=headers)
    html = etree.HTML(res.text)
    try:

        contents = html.xpath('//div[contains(@class, "userstuff")]/p/span[@class="md-plain"]/text()')
        content = "<br /><br />".join(contents)
        # print("1")
        if (content is None) or (re.sub(r"\s", "", content) == ""):
            # /works/19315723
            contents = html.xpath('//div[contains(@class, "userstuff")]/p/text()')
            content = "<br /><br />".join(contents)
            # print(content)
            if (content is None) or (re.sub(r"\s", "", content) == ""):
                contents = html.xpath('//div[contains(@class, "userstuff")]/div/p/text()')
                content = "<br /><br />".join(contents)

        # content = re.sub(r"\s", "", content)
        wrapper = [re.sub(r"<.+?>", " ", etree.tostring(x).decode("utf-8"))
                   for x in html.xpath('//dl[@class="work meta group"]/*')]
        newWrapper = [(x + ' ' + y) for (x, y) in zip(wrapper[0::2], wrapper[1::2])]
        # print(content)
        articleDetail = articleDetailItem()
        articleDetail.author = str(html.xpath('//h3[@class="byline heading"]/a/text()')[0])
        articleDetail.title = str(html.xpath('//h2[@class="title heading"]/text()')[0])

        try:
            articleDetail.chapterTitle = str(html.xpath('//h3[@class="title"]/a/text()')[0])
        except:
            articleDetail.chapterTitle = " "

        articleDetail.content = content
        articleDetail.wrapper = newWrapper
        articleDetail.url = url

        urls = {}
        urls['NextChapterURL'] = GetNextChapter(html)
        urls['PreviousChapterURL'] = GetPreviousChapter(html)
        urls['EntireChapterURL'] = GetEntireChapter(html)
        urls['ChapterIndexURL'] = GetChapterIndex(html)
        # print("urls:", urls)
        return articleDetail, urls

    except:
        try:
            new_href = str(
                html.xpath("//div[@id='outer']/div[@id='inner']/div[@id='main']/ul[@class='actions']/li[1]/a/@href")[0])
            url = "https://archiveofourown.org" + new_href
            res = requests.get(url=url, headers=headers)
            html = etree.HTML(res.text)
            contents = html.xpath('//div[contains(@class, "userstuff")]/p/span/text()')
            content = "<br /><br />".join(contents)
            # print("1")
            if (content is None) or (re.sub(r"\s|&nbsp;", "", content) == ""):
                # /works/19315723
                contents = html.xpath('//div[contains(@class, "userstuff")]/p/text()')
                content = "<br /><br />".join(contents)
                # print(content)
                if (content is None) or (re.sub(r"\s|&nbsp;", "", content) == ""):
                    contents = html.xpath('//div[contains(@class, "userstuff")]/div/p/text()')
                    content = "<br /><br />".join(contents)

            # content = re.sub(r"\s", "", content)
            wrapper = [re.sub(r"<.+?>", " ", etree.tostring(x).decode("utf-8"))
                       for x in html.xpath('//dl[@class="work meta group"]/*')]
            newWrapper = [(x + ' ' + y) for (x, y) in zip(wrapper[0::2], wrapper[1::2])]
            # print(content)
            articleDetail = articleDetailItem()
            articleDetail.author = str(html.xpath('//h3[@class="byline heading"]/a/text()')[0])
            articleDetail.title = str(html.xpath('//h2[@class="title heading"]/text()')[0])

            try:
                articleDetail.chapterTitle = str(html.xpath('//h3[@class="title"]/a/text()')[0])
            except:
                articleDetail.chapterTitle = " "

            articleDetail.content = content
            articleDetail.wrapper = newWrapper
            articleDetail.url = url

            urls = {}
            urls['NextChapterURL'] = GetNextChapter(html)
            urls['PreviousChapterURL'] = GetPreviousChapter(html)
            urls['EntireChapterURL'] = GetEntireChapter(html)
            urls['ChapterIndexURL'] = GetChapterIndex(html)
            # print("urls:", urls)
            return articleDetail, urls
        except:
            print("error")
            return None, None




def GetNextChapter(html):
    try:
        NextChapterURL = str(html.xpath("//li[@class='chapter next']/a/@href")[0])
        # menuBar = re.sub("work navigation actions", "btn-group", menuBar)
        # print("NextChapterURL")
        return NextChapterURL
    except:
        return None

def GetPreviousChapter(html):
    try:
        PreviousChapterURL = str(html.xpath("//li[@class='chapter previous']/a/@href")[0])
        # menuBar = re.sub("work navigation actions", "btn-group", menuBar)
        # print("PreviousChapterURL")
        return PreviousChapterURL
    except:
        return None

def GetEntireChapter(html):
    try:
        EntireChapterURL = str(html.xpath("//li[@class='chapter entire']/a/@href")[0])
        # menuBar = re.sub("work navigation actions", "btn-group", menuBar)
        # print("EntireChapterURL")
        return EntireChapterURL
    except:
        return None



def GetChapterIndex(html):
    try:
        ChapterIndexURL = etree.tostring(html.xpath("//li[@class='chapter']/noscript")[0]).decode("utf-8")
        # print(ChapterIndexURL)
        ChapterIndexURL = re.search(r'\"(.+?)\"', ChapterIndexURL).group(1)

        return ChapterIndexURL
    except:
        return None




if __name__ == '__main__':
    GetDetail(22478632)