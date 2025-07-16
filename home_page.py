import streamlit as st
import re
from parser import is_valid_cas

# Configure page settings
# st.set_page_config(
#     page_title="SDS GHS Extractor",
#     page_icon="🧪",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    invalid = False
    if "show_data_editor" not in st.session_state:
        st.session_state.show_data_editor = False

    st.header("Safety Data Sheet GHS Extractor")

    with st.form("all_data"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("Upload SDS Files")
            uploaded_pdfs = st.file_uploader("file_upload", type="pdf", accept_multiple_files=True, label_visibility="collapsed", key='uploaded')

        with col2:
            st.write("CAS Input")
            container = st.container(border=True, height=135)
            with container:
                container.write('Type in CAS numbers')
                container.caption("")
                pressed = st.form_submit_button("Input", use_container_width=False)
            if pressed:
                st.session_state.show_data_editor = not st.session_state.show_data_editor
            if st.session_state.show_data_editor:
                data = st.data_editor(use_container_width = True, data = {"CAS Number": [""]}, num_rows="dynamic", key='inputs')
                if data:
                    # print(data)
                    invalid_rows = []
                    for i, row in enumerate(data["CAS Number"]):
                        row = str(row)
                        if row == "":
                            continue
                        if not is_valid_cas(row):
                            invalid_rows.append((i, row))
                    if invalid_rows:
                        invalid = True
                        st.error(f"Invalid CAS Number(s): {', '.join(row for _, row in invalid_rows)}")
                    else:
                        invalid = False

        pressed = st.form_submit_button("Submit")
    if pressed:
        if invalid:
            print("invalid")
            pass
        else:
            print("valid")
            print(st.session_state.inputs)
            st.session_state.submitted = True
            st.rerun()
            pass

if st.session_state.submitted:
    print(st.session_state.uploaded)