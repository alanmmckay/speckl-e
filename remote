import time
import streamlit as st
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Set Meshy API key
meshy_api_key = "msy_vl1Dmn5G7LVZwuv8CvMpBLcQbGSZTx2xykLg"
headers = {
    "Authorization": f"Bearer {meshy_api_key}"
}

st.subheader("Inputs")

# Columns for inputs
serverCol, tokenCol = st.columns([1, 3])

# User Input boxes
speckleServer = serverCol.text_input("Server URL", "speckle.xyz", help="Speckle server to connect.")
speckleToken = tokenCol.text_input("Speckle token", "da1b5780f0f53e65b7f3a6b8601219f8cae43c3e76", help="If you don't know how to get your token, take a look at this [link](https://speckle.guide/dev/tokens.html)👈")

# Inputs for Meshy
object_prompt = st.text_input("Model Prompt:", "Describe the 3D model you want to generate...")
style_prompt = st.selectbox("Model Style:", ["realistic", "cartoon", "low-poly", "sculpture", "pbr"], help="Describe the style of the model.")
negative_prompt = st.text_input("Negative Prompt:", "low quality, low resolution, low poly, ugly", help="Describe what the texture should not look like.")
generate_button = st.button("Generate Model")
output_area = st.empty()
refresh_button = st.button("Refresh Page")

def generate_3d_model(object_prompt, style_prompt, negative_prompt):
    payload = {
        "mode": "preview",
        "prompt": object_prompt,
        "art_style": style_prompt,
        "negative_prompt": negative_prompt,
    }
    url = "https://api.meshy.ai/v2/text-to-3d"
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 202:
        task_id = response.json()['result']
        progress_bar = st.progress(0)
        while True:
            status_url = f"https://api.meshy.ai/v2/text-to-3d/{task_id}"
            status_response = requests.get(status_url, headers=headers)
            task_data = status_response.json()
            if task_data['status'] == 'SUCCEEDED':
                progress_bar.progress(100)
                return task_data
            elif task_data['status'] in ['FAILED', 'EXPIRED']:
                st.error("Task failed or expired.")
                return None
            else:
                progress_bar.progress(task_data['progress'])
                time.sleep(5)
    else:
        st.error(f"Error: {response.json().get('message', 'Unknown error')}")

def save_model_locally(obj_url):
    obj_data = requests.get(obj_url).content
    with open('model.obj', 'wb') as f:
        f.write(obj_data)
    return 'model.obj'

def save_model_to_speckle(file_path):
    f = open('model.obj','r')
    data = f.read()
    f.close()

    multipart_data = MultipartEncoder(
        fields={
            'file': ('model.obj', open('model.obj','rb'), 'text/plain')
            }
        )

    
    endpoint='https://app.speckle.systems/api/file/autodetect/bf02f1cbbc/main'

    files={
        "file": (open('model.obj','rb'))
    }

    headers={
        "Authorization" :"{}".format('da1b5780f0f53e65b7f3a6b8601219f8cae43c3e76')
    }

    response=requests.post(url=endpoint,headers=headers,files=files)

    if response.status_code == 200:
        print(response.content)
    else:
        response= response.text
        print(response)

def display_model(model_data):
    obj_url = model_data['model_urls']['obj']
    st.image(model_data['thumbnail_url'])
    local_path = save_model_locally(obj_url)
    
    st.download_button("Download OBJ", data=open(local_path, 'rb').read(), file_name="model.obj")
    save_model_to_speckle(local_path)

if generate_button:
    prompt = object_prompt
    style = style_prompt
    negative = negative_prompt
    model_data = generate_3d_model(prompt, style, negative)
    if model_data:
        display_model(model_data)
    else:
        st.error("Failed to generate the model.")

# Add refresh button functionality
if refresh_button:
    st.experimental_rerun()
