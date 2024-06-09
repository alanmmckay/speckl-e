#--------------------------
#IMPORT LIBRARIES
#import streamlit
import streamlit as st
import streamlit.components.v1 as components
# import streamlit.components.v1 as components
#specklepy libraries
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
from shape_e import generate_local_model
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

#--------------------------

#--------------------------
#PAGE CONFIG
st.set_page_config(
    page_title="Speckl-e uplaod utility",
    page_icon="📊"
)
#--------------------------

#--------------------------
#CONTAINERS
header = st.container()
input = st.container()
model = st.container()
embed_src = False;
#--------------------------

#--------------------------
#HEADER
#Page Header
with header:
    st.title("Speckl-E App")
#About info
with header.expander("About this app", expanded=True):
    st.markdown(
        """This streamlit app is an effort to discover the extent ant which
        specklepy features can be leveraged.
        """
    )
#--------------------------

with input:
    proceed = False
    st.subheader("Inputs")

    #-------
    #Columns for inputs
    serverCol, tokenCol = st.columns([1,3])
    #-------

	#User Input boxes
    speckleServer = serverCol.text_input("Server URL", help="Speckle server to connect.")
    #"3449a8170a0bd5f1b9c8a1c6c03e9fadbc91928b34"
    speckleToken = tokenCol.text_input("Speckle token", help="If you don't know how to get your token, take a look at this [link](<https://speckle.guide/dev/tokens.html>)👈")
    stream = False
    if speckleServer and speckleToken:
        try:
            client = SpeckleClient(host=speckleServer)
        #Get account from Token
            account = get_account_from_token(speckleToken, speckleServer)
        #Authenticate
            client.authenticate_with_account(account)        #Streams List👇
            streams = client.stream.list()

            #Get Stream Names
            streamNames = [s.name for s in streams]

            on = st.toggle("Use existing stream: ")

            if on:
                sName = st.selectbox(label="Select your stream", options=streamNames, index=None, help="Select your stream from the dropdown")
                if sName:
                    stream = client.stream.search(sName)[0]
                    stream_id = stream.id
                    proceed = True
            else:
                sName = st.text_input("Name of new Stream: ")
                if sName and sName not in streamNames:
                    try:
                        stream_id = client.stream.create(sName)
                        stream = client.stream.get(id=stream_id)
                        proceed = True
                    except:
                        st.markdown("Error in new stream branch")
                        proceed = False

        except Exception as e:
            st.markdown(''':red[Failure to connect. Please ensure server URL and Speckle Token are correct.]''')
            st.markdown(e)

    if stream:

        prompt = st.text_input("Prompt to generate new 3d model: ")

        ### call to function which generates a 3d model and places an obj file into the folder in which this script is run. The call to this function should also return the name of the file.
        obj_file = generate_local_model(prompt,stream_id)

        endpoint='https://app.speckle.systems/api/file/autodetect/'+stream_id+'/main'

        files={
            "file": (open(obj_file,'rb'))
        }

        headers={
            "Authorization" :"{}".format(speckleToken)
        }

        response=requests.post(url=endpoint,headers=headers,files=files)

        if response:
            print(stream)
            print(stream.id)
            embed_src = "https://speckle.xyz/embed?stream="+str(stream.id)
            print(embed_src)


with model:
    if embed_src:
        components.iframe(src=embed_src)
