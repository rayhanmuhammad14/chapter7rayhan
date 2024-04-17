from flask import Flask, render_template, request, jsonify,url_for
from pymongo import MongoClient

client = MongoClient('mongodb+srv://rayhan10915:Iw9flIHrKqSHga5a@learningx.cy1fhy8.mongodb.net/')
db = client.mydiary
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H:%m')
    return render_template('index.html', mytime=mytime)

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    file_recieve = request.files["file_give"]
    profile = request.files['profile_give']
    
    extension = file_recieve.filename.split('.')[-1]
    profileExt = profile.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'main-{mytime}.{extension}'
    profileName = f'profile-{mytime}.{profileExt}'
    
    save_to = f'static/img/{filename}'
    savePro = f'static/img/{profileName}'
    file_recieve.save(save_to)
    profile.save(savePro)
    

    doc = {
        'file' : filename,
        'profile' : profileName,
        'title':title_receive,
        'content':content_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    print(articles)
    return jsonify({'articles' : articles})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)