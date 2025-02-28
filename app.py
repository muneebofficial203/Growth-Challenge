# Imports
import streamlit as st
import pandas as pd
import os 
from io import BytesIO

# Set up app
st.set_page_config(page_title="🎉Data Sweeper Project", layout='wide')
st.title("✨Data Sweeper By Muneeb Khan")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)

if uploaded_files:
    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]

    for file in uploaded_files:
        # Convert BytesIO to file-like object with a name attribute
        file_name = file.name if hasattr(file, 'name') else 'uploaded_file'
        file_ext = os.path.splitext(file_name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display Info about files
        st.write(f"**File Name:** {file_name}")
        st.write(f"**File Size:** {file.size/1024} KB")

        # Show five rows of our dataframe
        st.write("Preview the head of a Dataframe")
        st.dataframe(df.head())

        # options for data cleaning 
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file_name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file_name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing values for {file_name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")

        # Choose specific columns to keep or convert
        st.subheader("🛠 Select Columns to convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)  
        df = df[columns]

        # Create some visualizations
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_df = df.select_dtypes(include='number').iloc[:, :2]
            if numeric_df.empty:
                st.write("No numeric columns available for visualization.")
            else:
                st.bar_chart(numeric_df)

        # Convert The file to csv or visa versa  
        st.subheader("🔂 Conversion Option")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()  # Initialize the buffer here
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"Download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🥳 All Files Processed!")
