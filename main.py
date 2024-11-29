from flask import Flask, request, jsonify, send_file
from io import BytesIO
import base64
from PIL import Image
import io

app = Flask(__name__)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    try:
        # Get the base64 string from the request data
        data = request.get_json()
        base64_image = data['image']

        # Decode the base64 image
        image_data = base64.b64decode(base64_image)

        # Convert the decoded data into an image
        image = Image.open(io.BytesIO(image_data))
        
        # Resize the image to 255x255 pixels
        image = image.resize((255, 255))

        # Save image into a BytesIO object to send it back
        img_io = BytesIO()
        image.save(img_io, 'PNG')  # Save as PNG or change format as needed
        img_io.seek(0)

        # Return the image as a response
        return send_file(img_io, mimetype='image/png')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)