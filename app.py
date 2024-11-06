from flask import Flask,render_template,request
import google.generativeai as genai
import os
import textblob
import sqlite3
import datetime


api = os.getenv("MAKERSUITE_API_KEY")
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main", methods=["GET","POST"])
def main():
    q = request.form.get("q")
    currentDateTime = datetime.datetime.now()
    conn = sqlite3.connect('userlog.db')
    c = conn.cursor()
    c.execute('INSERT INTO user (name,timestamp) VALUES(?,?)',(q,currentDateTime))
    conn.commit()
    c.close()
    conn.close()
    return(render_template("main.html"))

@app.route("/ai_agent", methods=["GET","POST"])
def ai_agent():
    return(render_template("ai_agent.html"))

@app.route("/ai_agent_reply", methods=["GET","POST"])
def ai_agent_reply():
    q = request.form.get("q")
    r = model.generate_content(q)
    return(render_template("ai_agent_reply.html",r=r.text))

@app.route("/prediction", methods=["GET","POST"])
def prediction():
    return(render_template("index.html"))

@app.route("/paynow", methods=["GET","POST"])
def paynow():
    return(render_template("paynow.html"))

@app.route("/SA", methods=["GET","POST"])
def SA():
    return(render_template("SA.html"))

@app.route("/SA_reply", methods=["GET","POST"])
def SA_reply():
    q = request.form.get("q")
    r = textblob.TextBlob(q).sentiment
    return(render_template("SA_reply.html",r=r))

@app.route("/userlog", methods=["GET","POST"])
def userlog():
    conn = sqlite3.connect('userlog.db')
    c = conn.cursor()
    c.execute('select * From user')
    r=""
    for row in c:
        print(row)
        r = r + str(row)
    c.close()
    conn.close()
    return(render_template("userlog.html",r=r))

if __name__ == "__main__":
    app.run()

