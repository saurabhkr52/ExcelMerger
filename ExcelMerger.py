import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

def clean_contact(contact):
    # Convert to string, remove spaces, keep only digits, get last 10 digits
    contact_str = str(contact).replace(" ", "")
    digits_only = ''.join(filter(str.isdigit, contact_str))
    return digits_only[-10:] if len(digits_only) >= 10 else digits_only

def prepare_cleaned_dataframe(merged_df, name_col, contact_col):
    cleaned_df = pd.DataFrame()
    cleaned_df['Name'] = merged_df[name_col].astype(str).str.strip()
    cleaned_df['Contacts'] = merged_df[contact_col].apply(clean_contact)
    return cleaned_df

def generate_excel_file(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='CleanedData')
    output.seek(0)
    return output

def main():
    st.set_page_config(page_title="📄 Pro Excel Cleaner", page_icon="✨", layout="centered")
    st.title("APNA LAPTOP Excel Merger and Cleaner")
    
    st.markdown("""
    Upload multiple Excel files, preview them, select your columns, clean the data perfectly, and download your file ready to use!
    """, unsafe_allow_html=True)

    st.divider()

    # ✨ Drag and Drop Upload
    uploaded_files = st.file_uploader(
        "📂 Drag and drop Excel files here",
        type=["xlsx"],
        accept_multiple_files=True,
        help="You can upload multiple .xlsx files."
    )

    if uploaded_files:
        st.success(f"🎉 {len(uploaded_files)} file(s) uploaded successfully!")

        with st.spinner("⏳ Merging your Excel files..."):
            dfs = [pd.read_excel(file) for file in uploaded_files]
            merged_df = pd.concat(dfs, ignore_index=True)

        st.subheader("👀 Preview Merged Data")
        st.dataframe(merged_df.head(10), use_container_width=True)

        all_columns = merged_df.columns.tolist()

        st.subheader("⚙️ Choose Columns to Clean")
        name_col = st.selectbox("📝 Select Name Column", all_columns)
        contact_col = st.selectbox("📞 Select Contacts Column", all_columns)

        if st.button("🚀 Clean and Generate File"):
            with st.spinner("✨ Cleaning and preparing your beautiful Excel file..."):
                cleaned_df = prepare_cleaned_dataframe(merged_df, name_col, contact_col)

            st.success("✅ Data cleaned successfully!")

            # 🎯 Live preview cleaned data
            st.subheader("🔍 Preview Cleaned Data")
            st.dataframe(cleaned_df.head(20), use_container_width=True)

            # Create Excel with timestamp
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cleanedData_{now}.xlsx"
            excel_file = generate_excel_file(cleaned_df)

            # st.balloons()  # 🎉 Cute Confetti Animation

            st.download_button(
                label="📥 Download Your Cleaned Excel",
                data=excel_file,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Click to download your cleaned Excel file."
            )

    else:
        st.info("📂 Please upload one or more Excel files to begin.")

if __name__ == "__main__":
    main()
