import streamlit as st
import subprocess
import tempfile
import os
import trimesh

# to run: streamlit run c:\Users\Minou\Desktop\convert.py

#--------------------------
# PAGE CONFIG
st.set_page_config(
    page_title="Speckl-e upload utility",
    page_icon="📊"
)
#--------------------------

# CONTAINERS
header = st.container()
input = st.container()
#--------------------------

#--------------------------
# HEADER
# Page Header
with header:
    st.title("Speckl-E upload App")
# About info
with header.expander("About this app", expanded=True):
    st.markdown(
        """This Streamlit app is an effort to discover the extent to which
        specklepy features can be leveraged.
        """
    )
#--------------------------

with input:
    st.subheader("Inputs")

    # File uploader
    uploaded_file = st.file_uploader("Upload an OBJ file", type=["obj"])

    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.obj') as temp_file:
            temp_file.write(uploaded_file.read())
            temp_obj_path = temp_file.name

        st.write(f"OBJ file uploaded: {temp_obj_path}")

        # Convert OBJ to STL
        mesh = trimesh.load(temp_obj_path)
        temp_stl_path = temp_obj_path.replace('.obj', '.stl')
        mesh.export(temp_stl_path)

        # Generate G-code using CuraEngine
        with tempfile.NamedTemporaryFile(delete=False, suffix='.gcode') as temp_gcode:
            temp_gcode_path = temp_gcode.name

        # Ensure CuraEngine is installed and accessible in your system's PATH
        # Customize the path to the CuraEngine executable as needed
        cura_engine_path = "C:\\Program Files\\UltiMaker Cura 5.7.2\\CuraEngine.exe"  # Replace with the actual path

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

            st.success("G-code generation successful!")
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
