import json, youtube_dl, magic, os
from flask import Flask, jsonify, send_file, request, make_response, Response
from pathlib import Path
from flask_cors import CORS, cross_origin
from .errors import errors

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(errors)

def donwloadMp3(url):
    info = youtube_dl.YoutubeDL().extract_info(url,download=False)
    title = info['title']
    title = title.replace(' ','_')
    print(title)
    os.system(f"youtube-dl -o 'mp3/{title}.%(ext)s' -i --extract-audio --audio-format mp3 --audio-quality 0 {url}")
    return info

def checkSameFile(name,mime):
    if mime == 'mp3':
        files = os.listdir('mp3')
        isSame = False
        for i in files:
            if i == name + '.mp3':
                isSame = True
                break
        return isSame
    elif mime == 'mp4':
        return False

def getTitle(url):
    info = youtube_dl.YoutubeDL().extract_info(url,download=False)
    return info['title'].replace(' ','_')

def getInfo(url):
    info = youtube_dl.YoutubeDL().extract_info(url,download=False)
    return info

@app.route('/api/mp3',methods=['GET'])
@cross_origin()
def getMp3():
    url = request.args.get('url')
    same = checkSameFile(getTitle(url),'mp3')
    response = None
    file = None
    print(same)
    app.logger.info(same)
    if same == False:
        response = donwloadMp3(url)
        file = response['title'] + ".mp3"
        file = file.replace(' ','_')
    else:
        file = getTitle(url).replace(' ','_') + ".mp3"
        response = getInfo(url)
    # return response
    return jsonify({

        "title":response['title'],
        "thumbnail":response['thumbnail'],
        "link":"127.0.0.1:5000/download?file=" + "mp3/" + file 

    })

@app.route('/download',methods=["GET"])
def download():
    file = request.args.get('file')
    file = os.path.join(file)
    try:
        return send_file(file, as_attachment=True,mimetype="audio/mpeg")
    except Exception as e:
        print(e)
        return jsonify({
            'error':'true'
            })

@app.route("/")
def index():
    return Response("Hello, world!", status=200)




@app.route("/health")
def health():
    return Response("OK", status=200)
