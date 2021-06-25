from flask import Flask
import matplotlib.image as mpimg
import requests,uuid
import json
import base64
import time
import urllib.request
from azure.storage.blob import BlobClient
UPLOAD_FOLDER = 'static/uploads/'


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
import os

import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        #filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        id = str(uuid.uuid1())+".jpg"
        blob = BlobClient.from_connection_string(
            conn_str="DefaultEndpointsProtocol=https;AccountName=imageclassification1;AccountKey=R0X33tP9FY0TfKwZ+O2BznpwDUZZWxbF2lJE3ToLhF4Dox/2V+frwVYUmEq3yDXAg+M5bszachzBpZDfT05CDA==;EndpointSuffix=core.windows.net",
            container_name="animals", blob_name=id)
        blob.upload_blob(file)
        # print('upload_image filename: ' + filename)

        s = 'https://imageclassification1.blob.core.windows.net/animals/' + str(id)
        webUrl = urllib.request.urlopen(s)
        data = webUrl.read()


        my_string = base64.b64encode(data)
        output = my_string.decode()

       # print(my_string)
        # Request data goes here
        data = {
            "Inputs": {
                "WebServiceInput0":
                    [
                        {
                            'image':output,
                            'id': "134",
                            'category': "dog",
                        },
                    ],
            },
            "GlobalParameters": {
            }
        }

        body = str.encode(json.dumps(data))

        url = 'http://71e1b67c-45c2-4302-ada7-97c53aef5b50.centralus.azurecontainer.io/score'
        api_key = 'rlr9B2b7ZkBoa7rAbBW7OWKeKEQ21gRJ'  # Replace this with the API key for the web service
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

        req = urllib.request.Request(url, body, headers)


        response = urllib.request.urlopen(req)

        result = response.read()






        flash(result)
        return render_template('index.html',filename=s)




@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run()