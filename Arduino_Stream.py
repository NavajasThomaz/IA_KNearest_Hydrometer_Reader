import requests  # to get image from the web
import shutil  # to save it locally


image_url = "http://192.168.0.189/capture?_cb=1655123939526"
filename = image_url.split("/")[-1]


def stream():
    r = requests.get(image_url, stream=True)
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open("Esp32-Cam\\TempPics\\frame.jpg", 'wb') as f:
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
        with open(f'Esp32-Cam\\TempFrames\\{name}.jpg', 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        return 1    #print('Image sucessfully Downloaded: ', filename)
    else:
        return print('Image Couldn\'t be retreived')

#stream()