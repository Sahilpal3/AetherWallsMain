from flask import Flask, jsonify, render_template, send_from_directory,request
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__,template_folder="midnight-horizons/templates",static_folder="midnight-horizons/static")

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

@app.route('/collection')
def collection():
    return render_template("midnight horizons.html")

#maps the directory for this method to upload folder specifically for HTTP POST requests
@app.route('/upload',methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error":"No image part"}), 400
    
    #Get the uploaded image and put it ithe file object
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error":"No selected File"}), 400
    
    if file and allowed_file(file.filename):
        #generate a name for the db
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        
        #save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],unique_filename)
        file.save(filepath)
        print(f"File saved at: {filepath}")
        
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
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    print("Found image files:", files)
    wallpapers = [
        {"filename":f,"alt":f.split('.')[0]} for f in files
        if allowed_file(f)
    ]
    return jsonify(wallpapers)
    
if __name__ == "__main__":
    app.run(debug=True)