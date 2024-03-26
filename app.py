# NOT OFFICIAL

from flask import Flask, render_template
app = Flask(__name__, static_url_path='/static/script.js')

@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run(debug=True ) 



# source used: https://medium.com/techcrush/how-to-render-html-file-in-flask-3fbfb16b47f6