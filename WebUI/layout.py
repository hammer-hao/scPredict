from browser import ajax, document, bind, window
from browser.html import *

url = "http://129.153.228.72/"

upload_button = INPUT('Upload file', id='upload', type='file', multiple="multiple")
send_file = BUTTON('send')
x = [i[0] for i in eval('[[0], [1], [2]]')]
print(x)
# upload_form = FORM()
# upload_form <= upload_button
document <= upload_button
document <= send_file


def upload_ok(req):
    print(req)
    print(req.text)
    document <= DIV(f'{req.text}')
    print('ok')


@bind(send_file, 'click')
def upload_file(ev):
    file = upload_button.files[0]
    ajax.file_upload(url, file,
                     field_name='file',
                     headers={"Content-Type": "multipart/form-data"},
                     oncomplete=upload_ok)

    print('ok')

