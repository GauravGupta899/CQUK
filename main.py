from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from helper import ImageQuantizer
from matplotlib.image import imread
from database import *
import os

# Flask setup
app = Flask(__name__)
app.secret_key = "top5"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        path = "static/uploads/"
        file.save(path+filename)  # Save the file
        size = os.path.getsize(path+filename)
        upload_obj = Upload(size=size, path="/"+path+filename)
        save_to_db(upload_obj)  # Save upload info to the database
        return redirect(url_for('gallery'))

@app.route('/gallery')
def gallery():
    db = get_db_session()
    uploads = db.query(Upload).all()
    return render_template('gallery.html', uploads=uploads)

@app.route('/quantized/gallery')
def quantized_gallery():
    db = get_db_session()
    results = db.query(Result).all()
    return render_template('qgallery.html', uploads=results)

@app.route('/quantize/<int:id>', methods=['GET', 'POST'])
def quantize(id):
    db = get_db_session()
    try:
        upload = db.query(Upload).get(id)  
        custom_image = imread(upload.path[1:])
        quantizer = ImageQuantizer(n_colors=int(request.args.get('colors')), image_path=upload.path[1:])
        quantizer.fit(custom_image)
        output = quantizer.save_results(custom_image)
        print(output)
        # save results
        save_to_db(
            Result(path="/"+output, size=os.path.getsize(output), ncolors=quantizer.n_colors)
        )
        flash("Color quantization on image was successful ", 'success')
        return redirect("/quantized/gallery")
    except Exception as e:
        print("Error:",e)
        flash(f"Error: {e} ", 'danger')
        return redirect("/gallery")

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    db = get_db_session()
    try:
        upload = db.query(Upload).get(id) 
        if upload:
            try: os.unlink(upload.path[1:])
            except:pass
            db.query(Upload).filter(Upload.id == id).delete()
            db.commit()
            db.close()
            flash("Image deleted", "success")
        else:
            flash("No image found in database", "danger")
    except Exception as e:
        print(e)
    finally:return redirect("/gallery")
            
@app.route('/delete/q/<int:id>', methods=['GET', 'POST'])
def qdelete(id):
    db = get_db_session()
    try:
        upload = db.query(Result).get(id) 
        if upload:
            try: os.unlink(upload.path[1:])
            except Exception as  e:print(e)
            db.query(Result).filter(Result.id == id).delete()
            db.commit()
            db.close()
            flash("Image deleted", "success")
        else:
            flash("No image found in database", "danger")
    except Exception as e:
        print(e)
    finally:return redirect("/quantized/gallery")

@app.route('/download/<int:id>', methods=['GET', 'POST'])
def download(id):
    db = get_db_session()
    try:
        upload = db.query(Upload).get(id)
        return send_file(upload.path[1:], download_name=os.path.basename(upload.path[1:]),as_attachment=True)
        return redirect('/gallery') 
    except Exception as e:
        print(e)

@app.route('/download/q/<int:id>', methods=['GET', 'POST'])
def qdownload(id):
    db = get_db_session()
    try:
        img = db.query(Result).get(id)
        return send_file(img.path[1:],download_name=os.path.basename(img.path[1:]),as_attachment=True )
        
    except Exception as e:
        print(e)
    

if __name__ == '__main__':
    app.run(debug=True)
