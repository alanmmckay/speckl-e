import time
import streamlit as st
import requests
import subprocess
import tempfile
import os
import trimesh

# Set Meshy API key
meshy_api_key = "msy_5GSF36dSBupG7NQV3UzmhvcrU60pNgu6Qwqr"
headers = {
    "Authorization": f"Bearer {meshy_api_key}"
}

st.set_page_config(
    page_title="3D Model Generator and Converter",
    page_icon="📊"
)

st.title("3D Model Generator and Converter")

# Initialize session state
if 'model_data' not in st.session_state:
    st.session_state['model_data'] = None

if 'glb_filename' not in st.session_state:
    st.session_state['glb_filename'] = 'model.glb'

if 'fbx_filename' not in st.session_state:
    st.session_state['fbx_filename'] = 'model.fbx'

if 'usdz_filename' not in st.session_state:
    st.session_state['usdz_filename'] = 'model.usdz'

if 'obj_filename' not in st.session_state:
    st.session_state['obj_filename'] = 'model.obj'

if 'mtl_filename' not in st.session_state:
    st.session_state['mtl_filename'] = 'model.mtl'

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

def display_model(model_data):
    model_url = model_data['model_urls']['glb']
    st.image(model_data['thumbnail_url'])

    st.text_input("GLB Filename:", st.session_state['glb_filename'], key='glb_filename_unique')
    st.text_input("FBX Filename:", st.session_state['fbx_filename'], key='fbx_filename_unique')
    st.text_input("USDZ Filename:", st.session_state['usdz_filename'], key='usdz_filename_unique')
    st.text_input("OBJ Filename:", st.session_state['obj_filename'], key='obj_filename_unique')
    st.text_input("MTL Filename:", st.session_state['mtl_filename'], key='mtl_filename_unique')

    st.download_button("Download GLB", data=requests.get(model_url).content, file_name=st.session_state['glb_filename'])
    st.download_button("Download FBX", data=requests.get(model_data['model_urls']['fbx']).content, file_name=st.session_state['fbx_filename'])
    st.download_button("Download USDZ", data=requests.get(model_data['model_urls']['usdz']).content, file_name=st.session_state['usdz_filename'])
    st.download_button("Download OBJ", data=requests.get(model_data['model_urls']['obj']).content, file_name=st.session_state['obj_filename'])
    st.download_button("Download MTL", data=requests.get(model_data['model_urls']['mtl']).content, file_name=st.session_state['mtl_filename'])

    if st.button("Convert OBJ to G-code for 3D Printing"):
        convert_to_gcode(model_data['model_urls']['obj'])

def calculate_filament_usage(gcode_path, layer_height, flow_modifier, extruder_diameter, filament_diameter):
    filament_volume = 0.0
    filament_radius = filament_diameter / 2

    with open(gcode_path, 'r') as file:
        for line in file:
            if line.startswith('G1'):
                parts = line.split(' ')
                line_length = 0.0
                for part in parts:
                    if part.startswith('E'):
                        line_length = float(part[1:])
                volume = layer_height * flow_modifier * extruder_diameter * line_length
                filament_volume += volume

    filament_length = filament_volume / (3.14159 * filament_radius * filament_radius)
    return filament_length

def convert_to_gcode(obj_url, layer_height=0.2, flow_modifier=1.0, extruder_diameter=0.4, filament_diameter=1.75):
    obj_data = requests.get(obj_url).content
    with tempfile.NamedTemporaryFile(delete=False, suffix='.obj') as temp_file:
        temp_file.write(obj_data)
        temp_obj_path = temp_file.name

    st.write(f"OBJ file saved: {temp_obj_path}")

    # Convert OBJ to STL
    mesh = trimesh.load(temp_obj_path)
    temp_stl_path = temp_obj_path.replace('.obj', '.stl')
    mesh.export(temp_stl_path)

    st.write(f"Converted to STL: {temp_stl_path}")

    # Generate G-code using CuraEngine
    with tempfile.NamedTemporaryFile(delete=False, suffix='.gcode') as temp_gcode:
        temp_gcode_path = temp_gcode.name

    # Ensure CuraEngine is installed and accessible in your system's PATH
    cura_engine_path = "C:\\Program Files\\UltiMaker Cura 5.7.2\\CuraEngine.exe"  # Ensure that cura_engine_path points to the correct location of your CuraEngine executable.

    try:
        subprocess.run([
            cura_engine_path, 
            "slice", 
            "-v", 
            "-j", "C:\\Users\\Minou\\Desktop\\Cura\\resources\\definitions\\fdmprinter.def.json",
            "-l", temp_stl_path,
            "-o", temp_gcode_path,
            "-s", "roofing_layer_count=5"  # Set roofing_layer_count to 5 or any appropriate number
        ], check=True)

        filament_length = calculate_filament_usage(temp_gcode_path, layer_height, flow_modifier, extruder_diameter, filament_diameter)
        st.success("G-code generation successful!")
        st.write(f"G-code generated: {temp_gcode_path}")
        st.write(f"Filament used: {filament_length:.2f} meters")

        # Replace old filament usage in the G-code file
        with open(temp_gcode_path, 'r') as gcode_file:
            gcode_lines = gcode_file.readlines()

        with open(temp_gcode_path, 'w') as gcode_file:
            for line in gcode_lines:
                if line.startswith(";Filament used:"):
                    gcode_file.write(f";Filament used: {filament_length:.2f} meters\n")
                else:
                    gcode_file.write(line)

        st.download_button(
            label="Download G-code",
            data=open(temp_gcode_path, 'rb').read(),
            file_name="output.gcode",
            mime="text/plain"
        )

    except subprocess.CalledProcessError as e:
        st.error(f"An error occurred while running CuraEngine: {e}")

    # Clean up temporary files
    os.remove(temp_obj_path)
    os.remove(temp_stl_path)
    os.remove(temp_gcode_path)

if generate_button:
    prompt = object_prompt
    style = style_prompt
    negative = negative_prompt
    model_data = generate_3d_model(prompt, style, negative)
    if model_data:
        st.session_state['model_data'] = model_data
        display_model(model_data)  # Display the model immediately after generation
else:
    if st.session_state['model_data']:
        display_model(st.session_state['model_data'])  # Display the model only if it's already present

# Add refresh button functionality
if refresh_button:
    st.experimental_rerun()
