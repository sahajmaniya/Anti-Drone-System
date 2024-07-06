from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils   import secure_filename
import tkinter as tk
from tkinter import messagebox
import os 

app = Flask(__name__)
# root = tk.Tk()
# root.withdraw()
app.config['SECRET_KEY']='superkey'
app.config['UPLOAD_FOLDER']='static/files'
class UploadFile(FlaskForm):
    file=FileField("File")
    submit=SubmitField("Upload File ")

@app.route('/', methods=['GET',"POST"])

@app.route('/index1.html', methods=['GET',"POST"])
def home():
    form=UploadFile()
    if form.validate_on_submit():
        file=form.file.data
        if(file):
           file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename )))
           return   render_template("index2.html",form=form) 
        return   render_template("index1.html",form=form) 
        
        
        # messagebox.showinfo("Alert", "This is an alert message!")
        # root.mainloop()
    return  render_template("index1.html",form=form)
 


if __name__ == '__main__':
    app.run(debug=True)
