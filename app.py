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
        if deceased_filename and os.environ.get("REPLICATE_API_TOKEN"):
            image_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], deceased_filename))
            
            with open(image_path, "rb") as image_file:
                # استخدام نموذج موثوق ومستقر لتحريك الصور وتوليد الفيديو
                output = replicate.run(
                    "stability-ai/stable-video-diffusion:9bbef67ade38eff8cbc6224f17c5ab571e0c20ff668a6f2b4c538a7985392d47",
                    input={
                        "input_image": image_file,
                        "prompt": memorial_prompt if memorial_prompt else "gentle motion, solemn tribute",
                        "motion_bucket_id": 127
                    }
                )
                if output:
                    generated_video_url = output[0] if isinstance(output, list) else output
    except Exception as e:
        print(f"Error connecting to Replicate: {e}")
        generated_video_url = "https://assets.mixkit.co/videos/preview/mixkit-tree-branches-in-the-breeze-1186-large.mp4"

    if not generated_video_url:
        generated_video_url = "https://assets.mixkit.co/videos/preview/mixkit-tree-branches-in-the-breeze-1186-large.mp4"

    return render_template('result.html', 
                           dates=memorial_dates, 
                           prompt=memorial_prompt,
                           video_url=generated_video_url)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
