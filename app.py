from flask import Flask, redirect, render_template, session,send_file, url_for,request
from importlib_metadata import method_cache
import os,io
from os.path import join, dirname,realpath
import pandas as pd
from werkzeug.utils import secure_filename
from works import *
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

app = Flask(__name__)

UPLOAD_FOLDER  = 'Desktop/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
option = 'TS'
data_filename  =''
app.secret_key = 'This is your secret key to utilize session in Flask'
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/merge", methods = ['POST'])
def upload_files():
    print(" + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +")
    uploaded_file1 = request.files['file1']
    uploaded_file2 = request.files['file2']
    uploaded_file3 = request.files['file3']
    if uploaded_file1.filename != '':
        file_path1 = os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file1.filename)
        print(file_path1)
        print(uploaded_file1)
        uploaded_file1.save(file_path1)
    if uploaded_file2.filename != '':
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file2.filename )
        uploaded_file2.save(file_path2)
    if uploaded_file3.filename != '':
        file_path3 = os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file3.filename )
        uploaded_file3.save(file_path3)
    else: file_path3 = ''
    merged_path = merge(file_path1,file_path2,file_path3)
    df = pd.read_csv(merged_path)
    print(df.info())
    session["df"] = df.to_csv(index=False,header=True,sep=",")
    df = session["df"] if "df" in session else ""
    buf_str = io.StringIO(df)
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))    
    return send_file(buf_byt,mimetype="text/csv",as_attachment=True,download_name="merged.csv")


def merge(file_path1,file_path2,file_path3):
    if file_path3 == '':
        merged = pd.concat(map(pd.read_csv,[file_path1,file_path2]),ignore_index=True)
    elif file_path3 != '':
        merged = pd.concat(map(pd.read_csv,[file_path1,file_path2]),ignore_index=True)
        merged.to_csv(UPLOAD_FOLDER+'merged.csv')
        merged = pd.concat(map(pd.read_csv,[UPLOAD_FOLDER+'merged.csv',file_path3]),ignore_index=True)
        merged.drop(merged.columns[0],axis=1,inplace=True)
    merged.to_csv(UPLOAD_FOLDER+'merged.csv', index = False)
    merged_path = UPLOAD_FOLDER+'merged.csv'
    print("This is merged path")
    print(merged_path)
    return merged_path

@app.route("/trim", methods = ['POST'])
def trim():
    print("Trim CSV Called")
    merged_file = request.files['merged']
    idle_time = request.form['idle_time']
    col_name = request.form['col_name']
    merged_filepath = os.path.join(app.config['UPLOAD_FOLDER'],merged_file.filename )
    merged_file.save(merged_filepath)
    isColumnPresent = checkColumnPresent(merged_filepath,col_name)
    if(isColumnPresent == 1):
        print("Column is Present")
        merged_path = trim_CSV(merged_filepath,idle_time,col_name)
        df = pd.read_csv(merged_path)
        print(df.info())
        session["df"] = df.to_csv(index=False,header=True,sep=",")
        df = session["df"] if "df" in session else ""
        buf_str = io.StringIO(df)
        buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
        print("trimCSV successfull")
        return send_file(buf_byt,mimetype="text/csv",as_attachment=True,download_name="trimmed.csv")
    elif(isColumnPresent == 0):
        print("Column Not Present")    
    return render_template('index.html',isPresent = isColumnPresent)
    
@app.route("/plot", methods = ['POST'])
def plot():
    file_to_plot = request.files['plot']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],file_to_plot.filename )
    heading = request.form['heading']
    x_axis = request.form['x_axis']
    y_axis = request.form['y_axis']
    file_to_plot.save(file_path)
    img_path = plot_csv(file_path,x_axis,y_axis,heading)
    print("plot csv call works")
    return render_template('plot_csv.html')
        
@app.route("/details", methods = ['POST'])
def csvDetails():
    print("Details Called")
    uploaded_df = request.files['detail_file']
    data_filename = secure_filename(uploaded_df.filename)
    print(uploaded_df)
    print(data_filename)
    uploaded_df.save(UPLOAD_FOLDER+data_filename)
    session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    data_file_path = session.get('uploaded_data_file_path', None)
    uploaded_df = pd.read_csv(data_file_path)
    uploaded_df_html = uploaded_df.to_html()
    no_of_columns = uploaded_df.shape[1] 
    return render_template('details.html', data = uploaded_df_html, df = uploaded_df, cols = no_of_columns)

@app.route("/edit", methods = ['POST','GET'])
def editCSV():
    print("Edit Called")
    return render_template('edit_csv.html')

@app.route("/editRows", methods = ['POST','GET'])
def editRows():
    print("Edit Rows Called")
    option = request.form['rem_add']
    strt_stp = request.form['start_stop']
    print(option)
    return render_template('edit_rows.html',remAdd = option,strt_stp = strt_stp)

@app.route("/deleteRows", methods = ['POST','GET'])
def deleteRows():
    uploaded_df = request.files['to_edit_file']
    time = request.form['time']
    data_filename = secure_filename(uploaded_df.filename)
    uploaded_df.save(UPLOAD_FOLDER+data_filename)
    session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    data_file_path = session.get('uploaded_data_file_path', None)
    removed_filepath = removeRowsFromStart(data_file_path,time)
    print(removed_filepath)
    df = pd.read_csv(data_file_path)
    session["df"] = df.to_csv(index=False,header=True,sep=",")
    df = session["df"] if "df" in session else ""
    buf_str = io.StringIO(df)
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
    return send_file(buf_byt,mimetype="text/csv",as_attachment=True,attachment_filename="removedFromStart.csv")

@app.route("/deleteFromMiddle", methods = ['POST','GET'])
def deleteFromMiddle():
    uploaded_df = request.files["to_edit_file"]
    from_time = request.form['from_time']
    to_time = request.form['to_time']
    data_filename = secure_filename(uploaded_df.filename)
    uploaded_df.save(UPLOAD_FOLDER+data_filename)
    session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    data_file_path = session.get('uploaded_data_file_path', None)
    removed_filepath = removeRowsFromMiddle(data_file_path,from_time,to_time)
    print(removed_filepath)
    df = pd.read_csv(data_file_path)
    session["df"] = df.to_csv(index=False,header=True,sep=",")
    df = session["df"] if "df" in session else ""
    buf_str = io.StringIO(df)
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
    return send_file(buf_byt,mimetype="text/csv",as_attachment=True,attachment_filename="removedInBetween.csv")   

@app.route("/deleteFromEnd", methods = ['POST'])
def deleteFromEnd():
    uploaded_df = request.files["to_edit_file"]
    time = request.form['time']
    data_filename = secure_filename(uploaded_df.filename)
    uploaded_df.save(UPLOAD_FOLDER+data_filename)
    session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    data_file_path = session.get('uploaded_data_file_path', None)
    removed_filepath = removeRowsFromEnd(data_file_path,time)
    print(removed_filepath)
    df = pd.read_csv(data_file_path)
    session["df"] = df.to_csv(index=False,header=True,sep=",")
    df = session["df"] if "df" in session else ""
    buf_str = io.StringIO(df)
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
    return send_file(buf_byt,mimetype="text/csv",as_attachment=True,attachment_filename="removedFromEnd.csv")   
    
@app.route("/editColumns",methods = ['POST'])
def editColumns():
    option = request.form['edit_col']
    print(option)
    return render_template('edit_columns.html',option = option,file = data_filename)

@app.route("/deleteColumns", methods = ['POST'])
def deleteColumns():
    print("Delete Columns Called")
    column_name = request.form['name_of_column']
    uploaded_df = request.files['to_edit_file']
    data_filename = secure_filename(uploaded_df.filename)
    uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))
    session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    data_file_path = session.get('uploaded_data_file_path', None)
    print(data_file_path)
    if(checkColumnPresent(data_file_path,column_name)):
        deleteColumn(uploaded_df,data_file_path,column_name)
        df = pd.read_csv(data_file_path)
        session["df"] = df.to_csv(index=False,header=True,sep=",")
        df = session["df"] if "df" in session else ""
        buf_str = io.StringIO(df)
        buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
        return send_file(buf_byt,mimetype="text/csv",as_attachment=True,attachment_filename="removedColumn.csv")   
    else :
        return render_template('edit_columns.html',deleted = 0,option = "delete_col")

@app.route("/resetColumn",methods=['POST'])
def resetColumn():
    print("Reset Columns Called")
    uploaded_df = request.files['to_edit_file']
    column_name = request.form['resetColumn']
    data_filename = secure_filename(uploaded_df.filename)
    uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))
    session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    data_file_path = session.get('uploaded_data_file_path', None)
    if(checkColumnPresent(data_file_path,column_name)):
        resetCol(data_file_path,column_name)
        df = pd.read_csv(data_file_path)
        session["df"] = df.to_csv(index=False,header=True,sep=",")
        df = session["df"] if "df" in session else ""
        buf_str = io.StringIO(df)
        buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
        return send_file(buf_byt,mimetype="text/csv",as_attachment=True,attachment_filename="resetColumn.csv")   
    else:
        return render_template('edit_columns.html',columnReseted = 0,option = "reset_col")

@app.route("/changeName",methods = ['POST'])
def changeName():
    print("Change Name Called")
    uploaded_df = request.files['to_edit_file']
    oldName = request.form['oldName']
    newName = request.form['newName']
    data_filename = secure_filename(uploaded_df.filename)
    uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))
    session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    data_file_path = session.get('uploaded_data_file_path', None)
    if(checkColumnPresent(data_file_path,oldName)):
        changeColumnName(data_file_path,oldName,newName)
        df = pd.read_csv(data_file_path)
        session["df"] = df.to_csv(index=False,header=True,sep=",")
        df = session["df"] if "df" in session else ""
        buf_str = io.StringIO(df)
        buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
        return send_file(buf_byt,mimetype="text/csv",as_attachment=True,attachment_filename="changedColumn.csv")   
    else:
        return render_template('edit_columns.html',columnChanged = 0, option="change_name") 

@app.route("/changeIndex",methods = ['POST'])
def changeIndex():
    print("Change Index Called")
    uploaded_df = request.files['to_edit_file']
    columnName = request.form['changeIndex']
    data_filename = secure_filename(uploaded_df.filename)
    uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))
    session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    data_file_path = session.get('uploaded_data_file_path', None)
    if(checkColumnPresent(data_file_path,columnName)):
        changeIndexColumn(data_file_path,columnName)
        df = pd.read_csv(data_file_path)
        session["df"] = df.to_csv(index=False,header=True,sep=",")
        df = session["df"] if "df" in session else ""
        buf_str = io.StringIO(df)
        buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
        return send_file(buf_byt,mimetype="text/csv",as_attachment=True,attachment_filename="changeIndex.csv")   
    else: 
        return render_template('edit_columns.html',indexChanged = 0,option = "change_index")

@app.route("/download")
def download():
    print("Download called")
    img = mpimg.imread('static/plot1.jpg')
    url = 'static/plot1.jpg'
    return send_file(url,as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)