from flask import Flask, render_template, request, redirect, url_for
import os
import replicate

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    generated_video_url = None
    
    try:
        # التحقق من توفر مفتاح الـ API ووجود الصورة
        if deceased_filename and os.environ.get("REPLICATE_API_TOKEN"):
            image_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], deceased_filename))
            
            with open(image_path, "rb") as image_file:
                output = replicate.run(
                    "stability-ai/stable-video-diffusion:3f0457b4619da651243f7627409249767e234857f62c0b5fdd086716a5a22d7d",
                    input={
                        "input_image": image_file,
                        "prompt": memorial_prompt if memorial_prompt else "animate naturally, solemn atmosphere",
                        "motion_bucket_id": 127
                    }
                )
                if output:
                    generated_video_url = output[0] if isinstance(output, list) else output
    except Exception as e:
        print(f"Error connecting to Replicate: {e}")
        # إذا حدث أي خطأ في الاتصال أو التوليد، نضع فيديو بديل مؤقت لكي لا يظهر خطأ 500 للمستخدم
        generated_video_url = "https://assets.mixkit.co/videos/preview/mixkit-tree-branches-in-the-breeze-1186-large.mp4"

    # إذا لم يتم توليد فيديو لأي سبب، نضع الفيديو البديل المؤقت
    if not generated_video_url:
        generated_video_url = "https://assets.mixkit.co/videos/preview/mixkit-tree-branches-in-the-breeze-1186-large.mp4"

    return render_template('result.html', 
                           dates=memorial_dates, 
                           prompt=memorial_prompt,
                           video_url=generated_video_url)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
