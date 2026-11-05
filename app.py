from flask import Flask,render_template
app = Flask(__name__)
@app.route('/lokesh/<int:id>')
def home(id):
  return f"my id is {id}"
@app.route('/home/<name>')
def std(name):
  return render_template('demo.html',name=name)
if __name__ == "__main__":
  app.run(debug=True)