#--------------------------
#IMPORT LIBRARIES
#import streamlit
import streamlit as st
# import streamlit.components.v1 as components
#specklepy libraries
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
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
viewer = st.container()
report = st.container()
graphs = st.container()
#--------------------------

#--------------------------
#HEADER
#Page Header
with header:
    st.title("Speckl-E upload  App")
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
    speckleServer = serverCol.text_input("Server URL", "speckle.xyz", help="Speckle server to connect.")
    #"3449a8170a0bd5f1b9c8a1c6c03e9fadbc91928b34"
    speckleToken = tokenCol.text_input("Speckle token", "3449a8170a0bd5f1b9c8a1c6c03e9fadbc91928b34", help="If you don't know how to get your token, take a look at this [link](<https://speckle.guide/dev/tokens.html>)👈")

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
                    print(stream.id)
                    proceed = True
            else:
                sName = st.text_input("Name of new Stream: ")
                if sName and sName not in streamNames:
                    try:
                        new_stream_id = client.stream.create(sName)
                        stream = client.stream.get(id=new_stream_id)
                        proceed = True
                    except:
                        st.markdown("Error in new stream branch")
                        proceed = False

        except Exception as e:
            st.markdown(''':red[Failure to connect. Please ensure server URL and Speckle Token are correct.]''')
            st.markdown(e)

    if proceed:
        proceed = False

        st.text_input("Prompt to generate new 3d model: ")


toggle = False

if toggle:
    #DEFINITIONS

    #create a definition that generates an iframe from commit id
    def commit2viewer(stream, commit, height=400) -> str:
        embed_src = "https://speckle.xyz/embed?stream="+stream.id+"&commit="+commit.id
        print(embed_src)
        return st.components.v1.iframe(src=embed_src, height=height)

    #VIEWER👁‍🗨
    with viewer:
        st.subheader("Latest Commit👇")
        commit2viewer(stream, commits[0])
    #--------------------------
