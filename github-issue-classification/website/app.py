#!/usr/bin/env python


import requests

from flask import Flask, request, render_template
app = Flask("Interactive Website")


@app.route('/', methods=['GET', 'POST'])
def homepage():
    input_text = None
    opt_text = None

    if request.method=="POST":
        input_text  = request.form["inputText"]
        response = requests.post('http://localhost:5059/github_issues/infer', json={'issue':str(input_text)})
        labels_json = response.json()
        labels = ', '.join(labels_json['label'][0])
        return render_template('homepage.html', outText = f"You submitted '{input_text}'", optText = labels)
    
    return render_template('homepage.html', outText = None, optText = None)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
