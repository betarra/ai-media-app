from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # استقبال البيانات النصية والوصف الجديد للذكريات
    text_prompt = request.form.get('text_prompt', '')
    memorial_dates = request.form.get('memorial_dates', '')
    memorial_prompt = request.form.get('memorial_prompt', '')
    animation_style = request.form.get('animation_style', '')
    image_prompt = request.form.get('image_prompt', '')

    print(f"النص الصوتي: {text_prompt}")
    print(f"تواريخ الذكرى: {memorial_dates}")
    print(f"وصف المشهد والملابس: {memorial_prompt}")
    print(f"نمط الحركة: {animation_style}")
    print(f"وصف الصورة: {image_prompt}")

    # استقبال جميع الملفات المحتمل رفعها (الصورة الشخصية، الصوت، صورة المتوفي، وصورة القبر)
    files_to_save = ['image', 'audio', 'deceased_image', 'grave_image']
    for file_key in files_to_save:
        if file_key in request.files:
            f = request.files[file_key]
            if f and f.filename != '':
                path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(path)
                print(f"تم حفظ الملف ({file_key}): {path}")

    return "<h3>تم استلام بيانات الذكريات والمشهد بنجاح! جاري معالجة التوليد...</h3>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
