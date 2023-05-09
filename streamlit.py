from docx_parser import Parser
import streamlit as st

@st.cache_data
def load_data():
    parser = Parser()
    return parser.return_map()

st.title("Text parser")

data_loading_state = st.text("parsing data")
data = load_data()
data_loading_state.text("Done.")

st.subheader("Parsed data:")
st.json(data)
    
