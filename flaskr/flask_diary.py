from flask import Flask,render_template,request,redirect,url_for
from getcontent import GetArticle
from getdetail import GetDetail

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/search')
def search():
    '''查询keyword'''
    keyword = request.args.get('keyword')
    articleList, pagenation, articleNumber = GetArticle(keyword)
    # return res
    return render_template('search.html',
                           articleList = articleList,
                           keyword=keyword,
                           pagenation=pagenation,
                           page=1,
                           articleNumber=articleNumber)

@app.route('/works/search')
def SearchByPage():
    '''查询keyword'''
    keyword = request.args.get('work_search[query]')
    print("keyword", keyword)
    page = request.args.get('page')
    articleList, pagenation, articleNumber = GetArticle(keyword, page)
    # return res
    return render_template('search.html',
                           articleList=articleList,
                           keyword=keyword,
                           pagenation=pagenation,
                           page=page,
                           articleNumber=articleNumber)


@app.route('/works/<int:id>/')
def diary_detail(id):
    articleDetail = GetDetail(id)

    return  render_template('articledetail.html', articleDetail=articleDetail)



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)