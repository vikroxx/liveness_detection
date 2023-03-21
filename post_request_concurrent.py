import requests
import concurrent.futures
from glob import glob
import time

def send_post_requests_concurrently(url, data_list, headers):
    # Create a function to send a single post request
    def send_post_request(data):
        response = requests.post(url, data=data, headers=headers)
        return response.text
    
    # Use concurrent.futures to execute multiple post requests in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the post requests to the executor
        futures = [executor.submit(send_post_request, data) for data in data_list]
        
        # Wait for all the requests to complete and collect the results
        results = [f.result() for f in futures]
        
    # Return the results
    return results


url = 'http://0.0.0.0:8000/liveness'
headers = {'Content-Type': 'image/jpeg'}

files =  glob('sample_images/*.jpeg') + glob('sample_images/*.jpg')
# Create a list of image data to send in the post requests
# data_list = [open('image1.jpg', 'rb').read(),
#              open('image2.jpg', 'rb').read(),
#              open('image3.jpg', 'rb').read()]

files = files * 10
print(len(files))
data_list = [open(file, 'rb').read() for file in files]
# data_list = [file for file in files]


# Send the post requests concurrently
t1= time.time()
results = send_post_requests_concurrently(url, data_list, headers)

print((time.time() - t1)*1000)
# Print the results
print(results)
print(len(results))