import os
import time
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

endpoint = os.getenv("BASE_URL")
key = os.getenv("API_KEY")

credentials = CognitiveServicesCredentials(key)

client = ComputerVisionClient(
    endpoint=endpoint,
    credentials=credentials
)

# def read_image(uri):
#     numberOfCharsInOperationId = 36
#     maxRetries = 10

#     # SDK call
#     rawHttpResponse = client.read(uri, language="en", raw=True)

#     # Get ID from returned headers
#     operationLocation = rawHttpResponse.headers["Operation-Location"]
#     idLocation = len(operationLocation) - numberOfCharsInOperationId
#     operationId = operationLocation[idLocation:]

#     # SDK call
#     result = client.get_read_result(operationId)
    
#     # Try API
#     retry = 0
    
#     while retry < maxRetries:
#         if result.status.lower () not in ['notstarted', 'running']:
#             break
#         time.sleep(1)
#         result = client.get_read_result(operationId)
        
#         retry += 1
    
#     if retry == maxRetries:
#         return "max retries reached"

#     if result.status == OperationStatusCodes.succeeded:
#         res_text = " ".join([line.text for line in result.analyze_result.read_results[0].lines])
#         return res_text
#     else:
#         return "error"

def read_image(image_path):
    numberOfCharsInOperationId = 36
    maxRetries = 10

    if os.path.isfile(image_path):  # Check if the input is a local file
        with open(image_path, "rb") as image_stream:
            # SDK call for local image file
            rawHttpResponse = client.read_in_stream(image_stream, language="en", raw=True)
    else:
        # Assume the input is a URI if it's not a local file
        rawHttpResponse = client.read(image_path, language="en", raw=True)

    # Get ID from returned headers
    operationLocation = rawHttpResponse.headers["Operation-Location"]
    idLocation = len(operationLocation) - numberOfCharsInOperationId
    operationId = operationLocation[idLocation:]

    # SDK call
    result = client.get_read_result(operationId)
    
    # Try API
    retry = 0
    while retry < maxRetries:
        if result.status.lower() not in ['notstarted', 'running']:
            break
        time.sleep(1)
        result = client.get_read_result(operationId)
        retry += 1
    
    if retry == maxRetries:
        return "max retries reached"

    if result.status == OperationStatusCodes.succeeded:
        res_text = " ".join([line.text for line in result.analyze_result.read_results[0].lines])
        return res_text
    else:
        return "error"
