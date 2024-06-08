import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

f = open('piparitalo1.obj','r')
data = f.read()
f.close()

multipart_data = MultipartEncoder(
    fields={
        'file': ('piparitalo1.obj', open('piparitalo1.obj','rb'), 'text/plain')
        }
    )

response = requests.post('https://speckle.xyz/api/file/3fd1b86931/main', data=multipart_data, headers={'token':'3449a8170a0bd5f1b9c8a1c6c03e9fadbc91928b34','Content-Type': multipart_data.content_type})

print(response)

response = requests.post('https://speckle.xyz/api/file/3fd1b86931/main', open('piparitalo1.obj','r'), headers={'token':'3449a8170a0bd5f1b9c8a1c6c03e9fadbc91928b34'})

print(response)

response = requests.post('https://speckle.xyz/streams/3fd1b86931/uploads', open('piparitalo1.obj','rb'), headers={'token':'3449a8170a0bd5f1b9c8a1c6c03e9fadbc91928b34'})

print(response)

endpoint='https://app.speckle.systems/api/file/autodetect/3fd1b86931/main'

files={
    "file": (open('piparitalo1.obj','rb'))
}

headers={
    "Authorization" :"{}".format('3449a8170a0bd5f1b9c8a1c6c03e9fadbc91928b34')
}

response=requests.post(url=endpoint,headers=headers,files=files)

if response.status_code == 200:
    print(response.content)


else:
    response= response.text
    print(response)
