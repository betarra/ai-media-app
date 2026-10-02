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
    # استقبال البيانات الجديدة والقديمة
    text_prompt = request.form.get('text_prompt')
    memorial_dates = request.form.get('memorial_dates')
    animation_style = request.form.get('animation_style')
    image_prompt = request.form.get('image_prompt')

    print(f"النص الصوتي: {text_prompt}")
    print(f"تواريخ الذكرى: {memorial_dates} | نمط الحركة: {animation_style}")
    print(f"وصف الصورة المراد توليدها: {image_prompt}")

    # استقبال الملفات إن وجدت
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file.filename != '':
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(image_path)
            print(f"تم حفظ الصورة: {image_path}")

    if 'audio' in request.files:
        audio_file = request.files['audio']
        if audio_file.filename != '':
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
            audio_file.save(audio_path)
            print(f"تم حفظ الصوت: {audio_path}")

    return "<h3>تم استقبال جميع البيانات والإعدادات بنجاح! جاري معالجة الطلب...</h3>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)