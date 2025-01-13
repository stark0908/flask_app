from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app=Flask(__name__)

def init_db():
    conn=sqlite3.connect("clipboard.db")
    cursor=conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clipboard(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   text TEXT NOT NULL,
                   code TEXT NOT NULL
    )
    """ )

    conn.commit()
    conn.close()

init_db()

@app.route('/clipboard/<userid>', methods=['GET','POST'])
def home(userid):
    conn=sqlite3.connect("clipboard.db")
    cursor=conn.cursor()
    
    if request.method=="POST":
        clipboard_text=request.form["clipboard_text"]

        #insert the data into the database
        
        cursor.execute("INSERT INTO clipboard (text,code) VALUES (?, ?)",(clipboard_text,userid))
        conn.commit()
        
        #return f"Text saved to clipboard: {clipboard_text}"
    
    cursor.execute("SELECT id,text FROM clipboard WHERE code=?",(userid,))
    all_texts=cursor.fetchall()
    conn.close()

    

    return render_template("clipboard_form.html",clipboard_entries=all_texts, user_code=userid)

@app.route('/delete/<userid>/<int:id>',methods=["POST"])
def delete(userid,id):
    conn=sqlite3.connect("clipboard.db")
    cursor=conn.cursor()

    #Delete the row with the matching id
    cursor.execute("DELETE FROM clipboard WHERE id=?",(id,))
    conn.commit()
    conn.close()


    return redirect(f"/clipboard/{userid}")

    
@app.route('/edit/<userid>/<int:id>',methods=['GET','POST'])
def edit(userid,id):
    conn=sqlite3.connect("clipboard.db")
    cursor=conn.cursor()

    if request.method =="POST":
        new_text=request.form["clipboard_text"]
        cursor.execute("UPDATE clipboard SET text=? WHERE id=?",(new_text,id))
        conn.commit()
        conn.close()
        
        return redirect(f"/clipboard/{userid}")
    cursor.execute("SELECT text FROM clipboard WHERE id=?",(id,))
    current_text=cursor.fetchone()[0]
    conn.close()

    return render_template("edit.html",current_text=current_text,id=id,user_code=userid)
    

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        user_code=request.form["code"]
        return redirect(f"/clipboard/{user_code}")

    return render_template('index.html')



if __name__=='__main__':
    app.run(debug=False)
