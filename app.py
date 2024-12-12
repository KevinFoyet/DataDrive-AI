import streamlit as st
from langchain.document_loaders.csv_loader import CSVLoader
import tempfile
from api import get_model_response

# Function to center the logo and title
def render_header():
    logo_path = r"https://raw.githubusercontent.com/KevinFoyet/DataDrive-AI/refs/heads/main/DataDrive%20AI%20Logo.webp" 

    # Center the logo and title
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.empty()
    with col2:
        st.image(logo_path, width=550, use_container_width=False)
        st.markdown("""
            <h1 style="text-align: center; color: #4CAF50;">DataDive AI</h1>
            <p style="text-align: center; font-size: 1.2em; color: #555;">
                Analyze your thousands of data in your CSV files by simply asking DataDive!
            </p>
            <hr style="border: 1px solid #4CAF50;">
        """, unsafe_allow_html=True)
    with col3:
        st.empty()

# Main function
def main():
    # Set page config for a wide layout
    st.set_page_config(page_title="DataDive AI", layout="wide")

    # Render the header with logo and title
    render_header()

    # Sidebar for file uploader
    st.sidebar.title("Upload Your CSV File")
    st.sidebar.markdown("""<p style="font-size: 1.1em; color: #555;">Select a CSV file to analyze</p>""", unsafe_allow_html=True)
    upload_file = st.sidebar.file_uploader("Choose a CSV File", type="csv")

    # Main section
    if upload_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(upload_file.getvalue())
            tmp_file_path = tmp_file.name

        # Initialize CSVLoader
        csv_loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
            'delimiter': ','
        })

        # Load data into the CSV loader
        data = csv_loader.load()

        # User query input
        st.markdown("""
            <h2 style="color: #4CAF50;">Ask Your Data</h2>
            <p style="color: #555;">Type your question below to start analyzing your data:</p>
        """, unsafe_allow_html=True)
        user_input = st.text_input("Your Question", placeholder="e.g., Which employee has the highest salary?")

        if user_input:
            # Display a spinner while processing
            with st.spinner("Analyzing your data..."):
                response = get_model_response(data, user_input)

            # Display the response in a styled card
            st.markdown(f"""
                <div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s; border-radius: 10px; padding: 20px; background-color: #f9f9f9; margin-top: 20px;">
                    <h4 style="color: #4CAF50;">Response</h4>
                    <p style="color: #333; font-size: 1.1em;">{response}</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
