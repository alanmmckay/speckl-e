3D Model Generator and Converter
================================

This project provides a web application for generating 3D models based on textual descriptions, converting them to different formats, and creating G-code for 3D printing. The application is built using Streamlit and integrates with the Meshy API for model generation.

Features
--------

- **Text-to-3D Model Generation**: Generate 3D models from textual prompts using the Meshy API.
- **Model Format Conversion**: Convert models to various formats including GLB, FBX, USDZ, OBJ, and MTL.
- **G-code Generation**: Convert OBJ files to G-code for 3D printing and calculate filament usage.
- **Download Options**: Download generated models in different formats.
- **Filament Usage Calculation**: Provides precise calculation of filament usage for 3D printing.

Prerequisites
-------------

- **Python 3.7 or higher**: Ensure you have a compatible version of Python installed.
- **Streamlit library**: Used for the web interface. Install using `pip install streamlit`.
- **requests library**: Required for making API calls. Install using `pip install requests`.
- **trimesh library**: Necessary for handling 3D models. Install using `pip install trimesh`.
- **Meshy API key**: Required for generating 3D models. Replace `meshy_api_key` in the code with your key.
- **CuraEngine**: Used for G-code generation. Ensure it’s installed and accessible in your system's PATH.

