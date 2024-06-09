Repository for the project labeled Speckl-e; a project created for the Beyond the Speckleverse hackathon. This includes two streamlit web apps which allows for the integration of Generative AI assets to be programatically be placed into the Speckle platform.

## Required files and libraries:

- Requires streamlit and specklepy.
    - using pip to install streamlit should work. This doesn't work for specklepy
    - To use specklepy, download the SDK code [here](https://github.com/specklesystems/specklepy)
        - Run through the [linked](https://python-poetry.org/docs/#installation) installation setup of **poetry**.
        - Place the files located in this repository within the SDK environment.
            - Navigate to this folder within the terminal and run the following command: `poetry run streamlit run speckl-e.py`

- Requires pytorch and shape_e to operate speckl_e-local.py
    - shap-e repository is located [here](https://github.com/openai/shap-e)

- Both speckl_e-local.py and speckle_e-remote.py will require a speckle access tokens as indicated within Speckle's API usage [documentation](https://speckle.systems/developers/apis/).
- Usage of speckle_e-remote.py will require an api key from Meshy. API documentation for Meshy is located [here](https://docs.meshy.ai/api-introduction)

## Repository Structure

- speckle_e-local.py: A strealit web-app which communicates to a local shap-e instance to generate 3d models.
    - shape_e.py: Parameter logic for shap_e to help produce local generative models. Requires a local instance of shap_e running with pytorch.
- speckle_e-remote.py: A streamlit web-app which communicates with the Meshy generative API to generate 3d models.
- extraneous_files/: Folder to house random bits of documentation used to help organize this hackathon project.
