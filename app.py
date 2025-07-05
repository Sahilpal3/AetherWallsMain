from flask import Flask, jsonify, render_template, send_from_directory,request,url_for
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3

app = Flask(__name__,template_folder="midnight-horizons/templates",static_folder="midnight-horizons/static")



#create a dictionary for collection data and the generate the page dynamically
collections={
        "echo-chamber":{
            "title":"Echo Chamber",
            "description":"A soundwave of visuals — curated wallpapers featuring iconic album covers, legendary artists, and the aesthetics of music culture across genres."
        },
        "dream-logic":{
            "title":"Dream Logic",
            "description":"Dive into the bizarre and beautiful. A surrealist gallery of wallpapers where reality bends, colors collide, and imagination reigns unfiltered."
        },
        "earthbound-eden":{
            "title":"Earthbound Eden",
            "description":"From secluded fjords to neon-lit cities — discover wallpapers capturing Earth's most cinematic locations, captured to feel like stills from a dream."
        },
        "pixel-pulse":{
            "title":"Pixel Pulse",
            "description":"A tribute to games that immerse you. Featuring atmospheric landscapes, character art, and UI-inspired designs from beloved titles."
        },
        "void-reverie":{
            "title":"Void Reverie",
            "description": "A cosmic blend of abstract minimalism, dark hues, and ambient textures — wallpapers that feel like they're dreaming in deep space."
        }
    }
    
#Confiugure upload Folder
#Specify folder to flask app
UPLOAD_FOLDER= os.path.join(app.static_folder, 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Creates the directory UPLOAD_FOLDER if it doesn't already exist, without raising an error if it does.
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

#Allowed image extensions
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','webp'}
def allowed_file(filename):
    #return true if file name  has . an its extension is allowed
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#This decorator maps the director /(Current directory to the function index)
@app.route('/')
def home():
    return render_template("index.html")

#dynamic route for any collection
@app.route('/collection/<collection_name>')
def collection_view(collection_name):
    
    data = collections.get(collection_name)
    if not data:
        return "Collection not Found", 404
    
    return render_template("collection_template.html",collection_name=collection_name,title=data["title"],description=data["description"])

#maps the directory for this method to upload folder specifically for HTTP POST requests
@app.route('/upload',methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error":"No image part"}), 400
    
    #Get the uploaded image and put it ithe file object
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error":"No selected File"}), 400
    
    #get author name(Default val unknows)
    author = request.form.get('author','unknown')
    
    #get tags
    tags = request.form.get('tags','')
    if file and allowed_file(file.filename):
        #generate a name for the db
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        collection = request.form.get('collection', 'uncategorized')
        
        #save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],unique_filename)
        file.save(filepath)
        print(f"File saved at: {filepath}")
        
        #save to DB
        conn = sqlite3.connect("wallpapers.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO wallpapers (filename, author, tags, collection) VALUES (?, ?, ?, ?)",(unique_filename, author, tags, collection))
        conn.commit()
        conn.close()
        
        return jsonify(
            {
                "message":"Uploaded Successfully!!",
                "filename": unique_filename,
                "url" : f"static/images/{unique_filename}"
            }
        ),200
    return jsonify({"error":"Filetype not allowed"}),400

print(f"Saving to: {UPLOAD_FOLDER}")
        
        
#dynamically serving the wallpapers
@app.route("/api/wallpapers")
def wallpapers():
    collection = request.args.get('collection',None)
    
    conn = sqlite3.connect('wallpapers.db')
    cur=conn.cursor()
    
    if collection:
        cur.execute("SELECT filename, author, tags FROM wallpapers WHERE collection = ?",(collection,))
    else:
        cur.execute("SELECT filename, author, tags FROM wallpapers")
        
    rows = cur.fetchall()
    
    wallpapers = [
        {
            "filename": row[0],
            "author": row[1],
            "tags": row[2].split(",") if row[2] else [],
            "alt":row[0].rsplit('.',1)[0].replace('_',' ').title()
        }
        for row in rows
        if allowed_file(row[0])
    ]
    
    return jsonify(wallpapers)
    
if __name__ == "__main__":
    app.run(debug=True)