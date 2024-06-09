import time
import streamlit as st
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Default Meshy API key
default_meshy_api_key = "msy_vl1Dmn5G7LVZwuv8CvMpBLcQbGSZTx2xykLg"

st.subheader("Inputs")

# Columns for inputs
serverCol, tokenCol, meshyCol = st.columns([1, 2, 2])

# User Input boxes
speckleServer = serverCol.text_input("Server URL", "speckle.xyz", help="Speckle server to connect.")
speckleToken = tokenCol.text_input("Speckle token", "da1b5780f0f53e65b7f3a6b8601219f8cae43c3e76", help="If you don't know how to get your token, take a look at this [link](https://speckle.guide/dev/tokens.html)👈")
meshy_api_key = meshyCol.text_input("Meshy API Key", default_meshy_api_key, help="Enter your Meshy API Key if different from the default.")

headers = {
    "Authorization": f"Bearer {meshy_api_key}"
}

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
    multipart_data = MultipartEncoder(
        fields={
            'file': ('model.obj', open(file_path, 'rb'), 'text/plain')
        }
    )

    endpoint = 'https://app.speckle.systems/api/file/autodetect/bf02f1cbbc/main'
    headers = {
        "Authorization": f"Bearer {speckleToken}",
        'Content-Type': multipart_data.content_type
    }

    response = requests.post(endpoint, data=multipart_data, headers=headers)

    if response.status_code in [200, 201]:
        st.success("Model uploaded to Speckle successfully.")
    else:
        st.error(f"Failed to upload model to Speckle. Status code: {response.status_code}")

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
