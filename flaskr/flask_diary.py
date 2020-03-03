from flask import Flask,render_template,request,redirect,url_for
from getcontent import GetArticle

app = Flask(__name__)

@app.route('/')
def index():
    # res = requests.get('https://archiveofourown.org/')
    # return res.text
    # getArticle()
    return render_template('index.html')

@app.route('/detail/<int:id>/')
def diary_detail(id):
    '''查询id'''
    pass
    # return  render_template('diary_detail.html',diary=diary)

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
#
# @app.route('/author/<name>/<int:pg>')
# def find_by_author(name=None,pg=None):
#     '''查询name'''
#     if pg is None:
#         pg = 1
#     if (name is None):
#         return redirect(url_for('index_diary'))
#     Diary_temp = Diary.query.filter_by(realname=name)
#     number = len(Diary_temp.all())
#     diary_list = Diary_temp.paginate(page=pg, per_page=10)
#     return  render_template("search.html", diary_list=diary_list, author_name=name, number=number)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)