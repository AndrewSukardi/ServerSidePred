from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
from fastapi.responses import StreamingResponse

app = FastAPI()

# Pydantic model to define the expected request structure
class ImageData(BaseModel):
    image_data: str

@app.post("/predict")
async def predict(data: ImageData):
    image_data = data.image_data

    try:
        # Decode the base64-encoded image data
        image_bytes = base64.b64decode(image_data)

        # Open the image from the decoded bytes
        image = Image.open(BytesIO(image_bytes))

        # Convert the image to a format that can be sent as a response (e.g., PNG)
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)

        # Return the image as a response using StreamingResponse
        return StreamingResponse(img_io, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=800)
