from flask import Flask
import flask
import uuid
import base64
import json
import glob
import yaml


app = flask.Flask(__name__)
urls = dict()

with open('data.json', 'r') as yf1:
    urls = json.load(yf1)


#with open('data.yaml', 'r') as yf1:
   # urls = yaml.load(yf1)

@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten():
    value = flask.request.form['url']
    if value == "":
        return flask.render_template('index.html')
    for k, v in urls.items():
        if v == value:
            return flask.redirect(flask.url_for('getvalue', k=k, preview=1))

    key = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:12].decode('ASCII')
    urls[key] = value

    with open('data.json', 'w') as f:
        json.dump(urls, f)

    return flask.redirect(flask.url_for('getvalue', k=key, preview=1))


@app.route('/<k>')
def getvalue(k):
    if k not in urls.keys():
        flask.abort(404)
    preview = flask.request.args.get('preview')
    value = urls[k]
    if preview == '1':
        return flask.render_template('output.html', key=k, value=value)
    return flask.redirect(value, code=301)

if __name__ == '__main__':
    app.run(debug=True)
