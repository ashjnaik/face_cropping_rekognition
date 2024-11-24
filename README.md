# face_cropping_rekognition

Here is a detailed step-by-step guide to set up this workflow on AWS Console in the Oregon region (us-west-2):

_Create an S3 Bucket_
Go to the S3 Console:
	•	Navigate to Amazon S3 Console.
	•	Ensure you are in the Oregon (us-west-2) region.

Create a bucket:
	•	Click Create bucket.
	•	Enter a bucket name (e.g., face-cropping-bucket).
	•	Select the Region: US West (Oregon).
	•	Enable Block Public Access settings (keep the bucket private).
	•	Click Create bucket.
Create Folders:
	•	In the bucket, create two folders:
	•	input/ (for unprocessed images).
	•	output/ (for processed images).


_Create an IAM Role for Lambda_
Go to the IAM Console:
	•	Navigate to IAM Console.
Create a Role:
	•	Click Roles > Create role.
	•	Select AWS Service and choose Lambda as the use case.
	•	Click Next.
Attach Policies:
	•	Attach the following managed policies:
	•	AmazonS3FullAccess (to read/write images to/from S3).
	•	AmazonRekognitionFullAccess (to use Rekognition for face detection).
	•	Click Next.
Review and Create:
	•	Enter a name for the role (e.g., lambda-s3-rekognition-role).
	•	Click Create role.


_Create a Lambda Function_
Go to the Lambda Console:
	•	Navigate to AWS Lambda Console.
Create Function:
	•	Click Create function.
	•	Choose Author from scratch.
	•	Enter the function name (e.g., process-image-function).
	•	Select Runtime: Python 3.9.
	•	Expand Permissions and choose the role you created earlier (lambda-s3-rekognition-role).
	•	Click Create function.
Configure the Function:
	•	In the Code Source section, paste the  Python code:
  Save the Function:
	•	Click Deploy to save the function.


Configure S3 Event Trigger
Add Trigger:
	•	Go to the Lambda function’s details page.
	•	Under Function overview, click Add trigger.
	•	Choose S3 as the trigger source.
Configure the Trigger:
	•	Bucket: Select your S3 bucket (e.g., face-cropping-bucket).
	•	Event type: Choose All object create events.
	•	Prefix: input/.
	•	Click Add.
 
_Test the Workflow_
Upload an Image:
	•	Upload an image to the input/ folder in your S3 bucket.
Check Results:
	•	The Lambda function will process the image, crop it, and save it to the output/ folder with _processed appended to the filename.
Monitor and Debug
	•	Use the CloudWatch Logs to monitor execution and debug errors.
	•	Go to CloudWatch Logs.
	•	Find your Lambda function logs under Log groups.
