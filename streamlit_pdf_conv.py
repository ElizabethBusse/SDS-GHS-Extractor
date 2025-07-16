# two options: SDS upload or CAS search
# collect all data that will be displayed onto streamlit UI

from parser import streamlit_pdf_upload
from test_parser import run_parser

def sds_upload(pdf_file):
    text = streamlit_pdf_upload(pdf_file)
    results = run_parser(input_val=text)
    return results