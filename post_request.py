import requests
from glob import glob
import time
# Set the API endpoint URL
url = 'http://0.0.0.0:8000/liveness'



# Open the image file and read the binary data
files =  glob('sample_images/*.jpeg') + glob('sample_images/*.jpg')

with open(files[0], 'rb') as f:
    image_data = f.read()

# Set the headers for the POST request
headers = {
    'Content-Type': 'image/jpeg'  # Set the content type to JPEG
}

t1 =  time.time()
# Send the POST request with the image data and headers
response = requests.post(url, data=image_data, headers=headers)
print( time.time() - t1)

print(response.status_code)
print(response.headers)
# Check the response status code
# if response.status_code == 200:
#     print('Image liveness score : {}'.format(response.))
# else:
#     print('Image upload failed.')
