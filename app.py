from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import uuid
import requests

app = Flask(__name__)

# Fetch random meme from Imgflip API
def fetch_meme():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    memes = response.json().get('data', {}).get('memes', [])
    if memes:
        meme = memes[0]# phli random image le lega url se
        return meme['url']
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    meme_url = None
    generated_meme_image = None

    if request.method == 'POST':
        top_text = request.form['top_text']# image parr top text dikhane ke leye
        bottom_text = request.form['bottom_text'] # image prr bottom text dikhane ke leye.
        image = request.files['image'] # requesting the image.

        img = Image.open(image)# function hai open krne ke leye
        draw = ImageDraw.Draw(img)
        
        # Use a default font if Arial is not available
        try:
            font = ImageFont.truetype("arial.ttf", size=int(img.height / 12))
        except IOError:
            font = ImageFont.load_default()

        def draw_text(text, y):
            # Use textbbox to get the width and height of the text (textsize ka replacement hai textbbox)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]  # Calculate width from bounding box
            x = (img.width - text_width) / 2
            draw.text((x, y), text, font=font, fill='white', stroke_width=2, stroke_fill='black')

        draw_text(top_text.upper(), 10)
        draw_text(bottom_text.upper(), img.height - int(img.height / 10))

        # Save the image to memory
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        generated_meme_image = img_io

    # Fetch random meme if the URL parameter 'fetch' is present
    if request.args.get("fetch") == "true":
        meme_url = fetch_meme()  # Get meme URL from API

    # Return the generated meme as a file object, which Flask can send directly
    if generated_meme_image:
        return send_file(generated_meme_image, mimetype='image/png')

    return render_template('index.html', meme_url=meme_url)

if __name__ == '__main__':
    app.run(debug=True)
