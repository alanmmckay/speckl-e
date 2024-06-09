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

---

## About our submission...

### Inspiration

Speckle as a platform sparked our interest in terms of its potential for providing a serializable repository of 3D models. The potential portability with existing and future connectors makes the framework an appealing place to collect these assets. Even though importing models created by humans is one way to fill a collection, there are still times when one may need to quickly produce a simple model. This brought about the idea of incorporating generative AI into Speckle.

Our preliminary discussion led us to believe this could become a useful tool for modelers and developers in any field. For example, a landscape architect who has been modeling a new college campus can be considered. Crafting and inserting every tree, rock, and bush by hand would take so much time, regardless of skill level. This is where our application shines. Developers will be free to focus on the centerpieces of their designs, while Speckl-e generates the supplementary assets to aid in their presentation. This saves time for an asset developer by having more tools accessible in one succinct software package.

### What it does

Our app leverages two methods for generating 3D object files. The first is by communication with Meshy, an enterprise-level generative AI service. This is via their API by passing text prompts from our app to their service. Meshy then converts these prompts into a 3D object file, passes it back to the user, and automatically uploads it into their Speckle stream. 

For users with the appropriate hardware and know-how, we incorporated a method of generating assets on your own device. Using OpenAI’s Shap-E, all of the asset generation can be done on your own GPU. This happens in real time, as demonstrated in our YouTube video. With either method, the models are uploaded to a Speckle stream. 

### How we built it

Speckle's guide LINK ME on creating a python streamlit app served as a scaffold for this project. Time was spent walking through the tutorial which then transitioned into looking at the graphQL sandbox. After achieving successful communication, we then began researching open-source 3D asset generators. Shap-E from openAI was discovered and chosen as our base model. As hardware concerns began to arise, we decided to implement an alternative application in tandem with the progress of leveraging Shap-E. This complementary implementation was built to connect to an enterprise-level AI that was hosted on dedicated hardware elsewhere.

### Challenges we ran into

Hardware was a big issue for generating local models. Only one member of our team had a Cuda-enabled device that could run Shap-E locally. Coordinating around this one device was a primary concern. We also had a difficult time finding documentation for more niche methods of communication with Speckle via an API. At the onset, we assumed that sending common 3D asset files through Speckle’s API would be straightforward, but we were unable to find any documentation or examples detailing how to do so. This forced us to resort to manually inspecting Specklepy’s general architecture whilst correlating our experiences using the graphQL API. We eventually found the restful endpoint, but it was only discovered through the support forums. 

### Accomplishments that we're proud of

One immediate success was in achieving communication directly from Speckle to Meshy and then back to Speckle. This was a huge milestone for the project. Next, getting Shap-E to run on our own hardware and return back to us the 3D files it generated demonstrated that our proof of concept would work. This changed how we view AI. When we think of generative AI, we typically think of large-scale data centers and subscription fees, but Shap-E enables users with moderate hardware to generate assets on their own. Years ago, we never would have believed AI could be this hands-on.

### What we learned

Three-dimensional assets are interesting to work with in Python. Peeling open a .obj file reveals that an asset contains much more information than an array of vertices. We used a tri-mesh class to examine the contents of such files and discovered that they naturally contain the rest of the requisite information like normal maps, faces, and colors. 

From a generative AI standpoint, creating three-dimensional assets from a text prompt is a remarkably challenging task, even as generative AI gains territory rapidly in other domains.  Generative AI models that produce images, like DALL-E, are part of the way there, in that they can take a relatively complicated text prompt and produce remarkable two-dimensional results. However, it’s difficult to represent three-dimensional assets in a way that is convenient for neural networks to work with. Open-AI’s Shap-E encodes three-dimensional assets into one-dimensional latents (essentially a vector) that is then an input into a conditioned diffusion model. The conditioned diffusion model works similarly to image generators, but instead of diffusing the elements of an image, elements of the encoded latent are diffused and then decoded to recover a 3D asset.   


### What's next for Speckl-e

It would be great to show our users their freshly produced assets in the app without having to navigate to Speckle (even though our app loads the assets directly into Speckle automatically). We were close to accomplishing this, but our lack of experience implementing streamlit ultimately presented a clear stopping point giver the duration of the project.

For the local asset generation, there are useful model parameters that can be considered. Shap-E can create multiple, unique inferences from a single text prompt since Shap-E is diffusion-based. Still, it would be nice for the user to have the option to generate multiple assets. Some of the finer points of the Shap-E model are also variable and can be fine-tuned to tweak the outputs. Something akin to an advanced menu that would allow the user to change default values would be of great use.

The field of state-of-the-art generative AI moves quickly. It is likely that our current implementation will become out of date and will need to be updated to keep up with advances in generating 3D assets from text prompts.  

We had an idea to make an app that uses the lidar sensors on our phones to scan objects in our surroundings and send those scans to speckle. This would further integrate tech into this package in a way that would be accessible to many users.

A data abstraction that can be leveraged to fine-tune an AI model. Here, multiple images can be generated for a given prompt where a user is only allowed to select one. This abstraction can be used to store these decisions to be used to train a model further.

