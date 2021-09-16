from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.wherewego

## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 캠핑 목록보기(Read) API
@app.route('/camping', methods=['GET'])
def view_campings():
    campInfos = list(db.campinfos.find({}, {'_id': False}))

    return jsonify({'campInfos': campInfos})


# 캠핑 목록 소팅(POST) - 도시
@app.route('/sort_city', methods=['POST'])
def sort_city():
    loc_receive = request.form['loc']
    camps = list(db.campinfos.find({}, {'_id': False}))

    sort_city = []

    for camp in camps:
        location = camp["location"]
        if loc_receive in location:
            sort_city.append(camp)

    return jsonify({'sort_city': sort_city})


# 캠핑 목록 소팅(POST) - 테마
@app.route('/sort_theme', methods=['POST'])
def sort_theme():
    theme_receive = request.form['theme']
    camps = list(db.campinfos.find({}, {'_id': False}))

    sort_theme = []

    for camp in camps:
        tag = camp["tag"]
        if theme_receive in tag:
            sort_theme.append(camp)

    for x in sort_theme:
        print(x)
    return jsonify({'sort_theme': sort_theme})


# 캠핑 목록 소팅(POST) - 리뷰수
@app.route('/sort_order', methods=['POST'])
def sort_view():
    order_receive = request.form['order']
    camps = list(db.campinfos.find({}, {'_id': False}))
    sort_order = []

    for camp in camps:
        camp['view'] = int(camp['view'])
    
    if order_receive == 'descending':
        sort_order = sorted(camps, key=(lambda x: x['view']), reverse=True)
        for x in sort_order:
            print(x)

    return jsonify({'sort_order': sort_order})


# 캠핑 리뷰저장(POST)
@app.route('/review', methods=['POST'])
def save_review():
    star = request.form['review_star']
    comment = request.form['review_comment']

    doc = {
        'star': star,
        'comment': comment,
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': '리뷰저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
