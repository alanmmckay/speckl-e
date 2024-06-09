import streamlit as st
import subprocess
import tempfile
import os
import trimesh
import numpy as np

def calculate_filament_length(gcode_path):
    """
    Calculate the total length of filament used by estimating the linear distance between coordinates in the G-code.
    """
    with open(gcode_path, 'r') as file:
        lines = file.readlines()

    total_distance = 0.0
    last_x, last_y = None, None

    for line in lines:
        if line.startswith('G1') and ('X' in line or 'Y' in line):
            coords = {part[0]: float(part[1:]) for part in line.split() if part[0] in 'XY'}
            x, y = coords.get('X', last_x), coords.get('Y', last_y)
            if last_x is not None and last_y is not None:
                total_distance += np.sqrt((x - last_x)**2 + (y - last_y)**2)
            last_x, last_y = x, y
    
    return total_distance  # in millimeters


# Start of Streamlit application
st.set_page_config(
    page_title="Speckl-e upload utility",
    page_icon="📊"
)

header = st.container()
input = st.container()

with header:
    st.title("Speckl-E upload App")
    with st.expander("About this app", expanded=True):
        st.markdown("This Streamlit app is an effort to discover the extent to which specklepy features can be leveraged.")

with input:
    st.subheader("Inputs")
    uploaded_file = st.file_uploader("Upload an OBJ file", type=["obj"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.obj') as temp_file:
            temp_file.write(uploaded_file.read())
            temp_obj_path = temp_file.name
        st.write(f"OBJ file uploaded: {temp_obj_path}")

        mesh = trimesh.load(temp_obj_path)
        temp_stl_path = temp_obj_path.replace('.obj', '.stl')
        mesh.export(temp_stl_path)
        st.write(f"Converted to STL: {temp_stl_path}")

        with tempfile.NamedTemporaryFile(delete=False, suffix='.gcode') as temp_gcode:
            temp_gcode_path = temp_gcode.name

        cura_engine_path = "C:\\Program Files\\UltiMaker Cura 5.7.2\\CuraEngine.exe"

        try:
            subprocess.run([
                cura_engine_path, 
                "slice", 
                "-v", 
                "-j", "C:\\Users\\Minou\\Desktop\\Cura\\resources\\definitions\\fdmprinter.def.json",
                "-l", temp_stl_path,
                "-o", temp_gcode_path,
                "-s", "roofing_layer_count=5"
            ], check=True)
            filament_length = calculate_filament_length(temp_gcode_path)
            st.success("G-code generation successful!")
            st.write(f"G-code generated: {temp_gcode_path}")
            st.write(f"Filament used: {filament_length:.2f} mm")
            st.download_button(
                label="Download G-code",
                data=open(temp_gcode_path, 'rb').read(),
                file_name="output.gcode",
                mime="text/plain"
            )
        except subprocess.CalledProcessError as e:
            st.error(f"An error occurred while running CuraEngine: {e}")

        os.remove(temp_obj_path)
        os.remove(temp_stl_path)
        os.remove(temp_gcode_path)
