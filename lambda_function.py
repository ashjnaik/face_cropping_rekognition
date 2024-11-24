import boto3
from PIL import Image, ImageDraw
import io

def detect_face(image_bytes):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_faces(Image={'Bytes': image_bytes}, Attributes=['ALL'])
    if response['FaceDetails']:
        return response['FaceDetails'][0]['BoundingBox']
    else:
        raise ValueError("No face detected.")

def crop_and_process_image(image_bytes, bounding_box, output_size=150, padding_factor=1.5):
    image = Image.open(io.BytesIO(image_bytes))
    width, height = image.size
    left = int(bounding_box['Left'] * width)
    top = int(bounding_box['Top'] * height)
    box_width = int(bounding_box['Width'] * width)
    box_height = int(bounding_box['Height'] * height)
    padding = int(box_height * padding_factor)
    crop_left = max(0, left - padding)
    crop_top = max(0, top - padding)
    crop_right = min(width, left + box_width + padding)
    crop_bottom = min(height, top + box_height + padding)
    cropped_image = image.crop((crop_left, crop_top, crop_right, crop_bottom))
    resized_image = cropped_image.resize((output_size, output_size), Image.LANCZOS)
    mask = Image.new("L", (output_size, output_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, output_size, output_size), fill=255)
    circular_image = Image.new("RGBA", (output_size, output_size), (255, 255, 255, 0))
    circular_image.paste(resized_image, (0, 0), mask)
    buffer = io.BytesIO()
    circular_image.save(buffer, format="PNG")
    return buffer.getvalue()
    
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    if not object_key.startswith("input/"):
        return {"statusCode": 400, "body": "File not in input folder."}
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    image_bytes = response['Body'].read()
    try:
        bounding_box = detect_face(image_bytes)
        processed_image = crop_and_process_image(image_bytes, bounding_box)
        output_key = object_key.replace("input/", "output/").replace(".png", "_processed.png")
        s3.put_object(Bucket=bucket_name, Key=output_key, Body=processed_image, ContentType="image/png")
        return {"statusCode": 200, "body": f"Processed image saved to {output_key}"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}


