from flask import Flask, render_template,request,send_file
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import parser
import logging

app = Flask(__name__)

@app.route("/")

@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/download")
def download():
    return send_file('result.csv',as_attachment=True)


@app.route("/parse", methods=['POST'])
def parse():
    try:
        if request.method == 'POST':
            url = request.form["url_input"]

            if not parser.check_http_returncode(str(url)):
                exit()
    
            res_dict = {'Название': [], 'Цена': [], 'Описание': []}

            soup = bs(requests.get(url).text, "html.parser")
            parser.get_names(soup, res_dict)
            parser.get_prices(soup, res_dict)
            parser.get_descriptions(soup, res_dict)

            csv_table = pd.DataFrame(res_dict)
            csv_table.to_csv('result.csv', encoding='utf-16') 

            return download()

    except requests.exceptions.MissingSchema: 
        app.logger.error("url is empty")
        return index()
