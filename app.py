from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'  # نقلناها إلى static لكي يمكن عرضها في المتصفح مباشرة
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    memorial_dates = request.form.get('memorial_dates', '')
    memorial_prompt = request.form.get('memorial_prompt', '')
    
    saved_files = {}
    files_to_save = ['image', 'audio', 'deceased_image', 'grave_image']
    
    for file_key in files_to_save:
        if file_key in request.files:
            f = request.files[file_key]
            if f and f.filename != '':
                path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(path)
                saved_files[file_key] = f.filename

    # تمرير الصور والبيانات إلى صفحة النتيجة المحترمة
    return render_template('result.html', 
                           dates=memorial_dates, 
                           prompt=memorial_prompt,
                           deceased=saved_files.get('deceased_image'),
                           grave=saved_files.get('grave_image'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
