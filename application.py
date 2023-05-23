from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import sys
import csv
from source.exceptions import CustomException as exc


# import source.logger 
application = Flask(__name__)
app = application

@app.route('/', methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['search'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            # t.logging.info("request get from user")
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            # t.logging.info("product found")
            print(productLink)
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            name = prod_html.find('span', {'class':"B_NuCI"}).contents[0]
            rating=prod_html.find('div',{'class':"_3LWZlK"})
            try:
                rating=rating.text
                print(rating)
            except AttributeError as e:
                print("no reviwe yet")
                # t.logging.info("error ocuures fetching reviews")
            try:
                ul = prod_html.find(class_="_2418kt")
                highlight = ""
                # extract the li elements from the ul element
                li_list = ul.find_all("li") if ul else []
                # loop through the li elements and extract their text content
                for li in li_list:
                    highlight += li.text.strip() 
                # print the extracted text
                print(highlight)
            except AttributeError as e:
                # t.logging.info("error ocuures while fetching highlight")
                print("no highlight")
                highlight="no highlight"
            

            SP=prod_html.find("div",{"class":"_30jeq3 _16Jk6d"}).text
            MRP=prod_html.find("div",{"class":"_3I9_wc _2p6lqe"}).text
            description=[]
            # filename = searchString + ".csv"
            # fw = open(filename, "w")
            # headers = "name,reviews,selling price,MRP,ProductLink,highlight \n"
            # fw.write(headers)
            
            mydict = {"name": name, "rating": rating,"selling price":SP,"MRP":MRP, "productLink": productLink, "highlight": highlight}
            description.append(mydict)
            filename = searchString + ".csv"
            with open(filename, "w", encoding="utf-8", newline="") as fw:
                headers = ["product name", "rating", "selling price", "MRP", "ProductLink", "highlight"]
                csv_writer = csv.writer(fw)
                csv_writer.writerow(headers)
                for item in description:
                    row = [item["name"], item["rating"], item["selling price"], item["MRP"], item["productLink"], item["highlight"]]
                    csv_writer.writerow(row)
            t.logging.info("program excecuted succefully")
            return render_template('results.html', results=description)
        except Exception as e:
            error_message=exc(e,sys)
            print(error_message)
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
   