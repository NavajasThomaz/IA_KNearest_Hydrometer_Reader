import requests  # to get image from the web
import shutil  # to save it locally

## Set up the image URL and filename
image_url = "http://192.168.0.143/capture?_cb=1652447966560"
filename = image_url.split("/")[-1]

# Open the url image, set stream to True, this will return the stream content.
def stream():
    r = requests.get(image_url, stream=True)
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open("C:\\Users\\AUGEN12\\PycharmProjects\\HidroReader\\Esp32Pics\\Pics\\frame.jpg", 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        return print('Image sucessfully Downloaded: ', filename)
    else:
        return print('Image Couldn\'t be retreived')

def streamVid(name):
    r = requests.get(image_url, stream=True)
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(f"C:\\Users\\AUGEN12\\PycharmProjects\\HidroReader\\Esp32Pics\\Videos\\Temp\\{name}.jpg", 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        return print('Image sucessfully Downloaded: ', filename)
    else:
        return print('Image Couldn\'t be retreived')

#stream()