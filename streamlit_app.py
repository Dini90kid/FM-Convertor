import streamlit as st
from agent_fm import parse_fm_source, generate_json_spec, generate_markdown_doc, generate_python_stub, generate_pytest_stub

st.set_page_config(page_title="FM Converter", layout="centered")

st.title("ABAP FM Converter")
st.write("Upload an ABAP Function Module source file to generate JSON specification, Markdown docs, Python stub code, and optional pytest stub.")

uploaded = st.file_uploader("Upload ABAP Function Module source (.abap or .txt)", type=["abap", "txt"])

include_pytest = st.checkbox("Generate pytest stub", value=False)

if uploaded:
    src = uploaded.read().decode("utf-8", errors="ignore")

    try:
        fm = parse_fm_source(src)
    except Exception as e:
        st.error(f"Parsing error: {e}")
        st.stop()

    st.subheader("Parsed Function Module")
    st.json(fm)

    # JSON spec
    json_spec = generate_json_spec(fm)
    st.download_button("Download JSON Spec", json_spec, "fm_spec.json", "application/json")

    # Markdown doc
    md_doc = generate_markdown_doc(fm)
    st.download_button("Download Markdown Documentation", md_doc, "fm_doc.md", "text/markdown")

    # Python stub
    py_stub = generate_python_stub(fm)
    st.download_button("Download Python Stub", py_stub, "fm_stub.py", "text/plain")

    # pytest stub (optional)
    if include_pytest:
        pytest_stub = generate_pytest_stub(fm)
        st.download_button("Download pytest Stub", pytest_stub, "test_fm_stub.py", "text/plain")
