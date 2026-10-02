from flask import Flask, render_template, request, redirect, url_for
import os
import replicate

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ضع مفتاح Replicate الخاص بك هنا، أو قم بتعيينه كمتبيّن بيئة (Environment Variable) في Render باسم REPLICATE_API_TOKEN
# os.environ["REPLICATE_API_TOKEN"] = "رอน_المفتاح_الخاص_بك_هنا"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    memorial_dates = request.form.get('memorial_dates', '')
    memorial_prompt = request.form.get('memorial_prompt', '')
    
    deceased_filename = None
    if 'deceased_image' in request.files:
        f = request.files['deceased_image']
        if f and f.filename != '':
            path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(path)
            deceased_filename = f.filename

    # رابط الصورة المحلي أو العام الذي سيتم إرساله للذكاء الاصطناعي
    # (ملاحظة: في بيئة الإنتاج على Render، يفضل استخدام رابط عام، ولكن سنجرب تشغيل النموذج عبر Replicate)
    generated_video_url = None
    
    try:
        if deceased_filename:
            # مثال لنموذج توليد فيديو من صورة ووصف (Image-to-Video) على Replicate
            # نموذج Stable Video Diffusion أو ما يشابهه
            image_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], deceased_filename))
            
            # سنستخدم نموذج استقرار الفيديو أو محاكاة الحركة بناءً على الوصف
            # ملاحظة: يتطلب تشغيل هذا وجود رصيد تجريبي أو حقيقي في حسابك على Replicate.com
            with open(image_path, "rb") as image_file:
                output = replicate.run(
                    "stability-ai/stable-video-diffusion:3f0457b4619da651243f7627409249767e234857f62c0b5fdd086716a5a22d7d",
                    input={
                        "input_image": image_file,
                        "prompt": memorial_prompt if memorial_prompt else "animate naturally, smiling, waving hand",
                        "motion_bucket_id": 127
                    }
                )
                if output:
                    generated_video_url = output[0] if isinstance(output, list) else output
    except Exception as e:
        print(f"Error generating AI video: {e}")
        # إذا حدث خطأ في التوليد (بسبب عدم توفر مفتاح أو رصيد)، سنضع فيديو افتراضي مؤقت لكي لا يتعطل الموقع
        generated_video_url = "https://assets.mixkit.co/videos/preview/mixkit-tree-branches-in-the-breeze-1186-large.mp4"

    return render_template('result.html', 
                           dates=memorial_dates, 
                           prompt=memorial_prompt,
                           video_url=generated_video_url)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
