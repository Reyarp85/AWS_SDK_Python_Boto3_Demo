import os
from flask import Flask, render_template, request, redirect, url_for, session
import boto3
from botocore.exceptions import ClientError
import uuid

app = Flask(__name__)

# TODO: Create a S3 bucket to be used?

# export S3_BUCKET_NAME=albertleng-aws-sdk-boto3
S3_BUCKET = os.environ.get('S3_BUCKET_NAME')

# export SECRET_KEY=test_key
app.secret_key = os.environ.get('SECRET_KEY')

s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')


def generate_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={
                                                        'Bucket': bucket_name,
                                                        'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None
    return response


@app.route('/')
def index():
    return render_template('index.html')


# TODO: Use Postman to demo also
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(url_for('index'))

    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('index'))

        # Check if the file extension is supported
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    if file.filename.split('.')[-1].lower() not in allowed_extensions:
        session['error_message'] = ("Unsupported file format. "
                                    "Please upload a JPG or PNG image.")
        return redirect(url_for('index'))

    filename = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1]

    s3_client.upload_fileobj(file, S3_BUCKET, filename, ExtraArgs={
        'ContentType': file.content_type})

    response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket': S3_BUCKET, 'Name': filename}},
        MaxLabels=10
    )

    labels = [
        {"name": label['Name'], "confidence": f"{label['Confidence']:.2f}"} for
        label in response['Labels']]

    # Detect text in the image
    text_response = rekognition_client.detect_text(
        Image={'S3Object': {'Bucket': S3_BUCKET, 'Name': filename}}
    )

    # Extract detected text
    detected_text = [text['DetectedText'] for text in
                     text_response['TextDetections'] if text['Type'] == 'LINE']

    image_url = generate_presigned_url(S3_BUCKET, filename)

    return render_template('result.html', labels=labels, image_url=image_url,
                           detected_text=detected_text)


if __name__ == '__main__':
    app.run(debug=True)
