# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for
from getcontent import GetArticle
from getdetail import GetDetail
from get_author import GetAuthorWorks
import re
import sys
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/search')
def Search():
    '''查询keyword'''
    keyword = request.args.get('keyword')
    articleList, pagenation, articleNumber = GetArticle(keyword)
    # return res
    return render_template(
        'search.html',
        articleList = articleList,
        keyword=keyword,
        pagenation=pagenation,
        page=1,
        articleNumber=articleNumber
    )

@app.route('/works/search')
def SearchByPage():
    '''查询keyword'''
    keyword = request.args.get('work_search[query]')
    print("keyword", keyword)
    page = request.args.get('page')
    articleList, pagenation, articleNumber = GetArticle(keyword, page)
    # return res
    if not pagenation:
        page = 1
    return render_template(
        'search.html',
        articleList=articleList,
        keyword=keyword,
        pagenation=pagenation,
        page=page,
        articleNumber=articleNumber
    )


@app.route('/works/<int:id>/')
@app.route('/works/<int:id>')
def ArticleDetail(id):
    full = request.args.get("view_full_work")
    if full == 'true':
        articleDetail, urls = GetDetail(id, full=full)
        full = True
    else:
        articleDetail, urls = GetDetail(id)
        full = False
    if articleDetail is None:
        return render_template('404.html')
    else:
        return render_template(
            'articledetail.html',
            articleDetail=articleDetail,
            urls=urls,
            full=full,
            rawurl=re.sub(r"\?.+?$","",request.url)
        )


@app.route('/works/<int:id>/chapters/<int:chapter>/')
@app.route('/works/<int:id>/chapters/<int:chapter>')
def ArticleChapter(id, chapter):
    articleDetail, urls = GetDetail(id, chapter=chapter)
    full = False
    if articleDetail is None:
        return render_template('404.html')
    else:
        return render_template(
            'articledetail.html',
            articleDetail=articleDetail,
            urls=urls,
            full=full,
            rawurl=re.sub(r"\?.+?$","",request.url)
        )

@app.route('/users/<name>')
def GetAuthor(name):
    pass



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)