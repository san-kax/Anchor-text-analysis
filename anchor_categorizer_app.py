import streamlit as st
import pandas as pd
import os
import io
from urllib.parse import urlparse
from tqdm import tqdm

st.set_page_config(page_title="Anchor Categorizer", layout="centered")

def get_main_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def categorize_anchors_df(df, file_name):
    try:
        if 'Anchor' not in df.columns or 'Target URL' not in df.columns:
            st.warning(f"❌ Skipping {file_name}: Required columns not found.")
            return None
        
        anchors_in_file = df['Anchor'].dropna().str.lower()
        target_url = df['Target URL'].iloc[0]

        main_domain = get_main_domain(target_url)
        root_domain = main_domain.split('.')[0]

        branded_variants = [main_domain, root_domain]

        exact_match_anchors = [
            "online casino uk", "uk casino", "casino sites", "best online casino", "casino uk",
            "casino online uk", "online casinos uk", "online casinos", "best online casino uk",
            "casino sites uk", "casinos", "uk casino sites", "best casino sites", "uk online casino",
            "casinos online", "uk casinos", "top 50 online casinos uk", "best online casinos",
            "casino uk online", "casino games uk", "best uk casino", "online casinos in uk", "best casino",
            "uk online casinos list", "best casino online", "best casino uk", "top 20 online casinos uk",
            "uk casino online", "casinos uk", "best online casinos uk", "best uk online casino",
            "online uk casino", "uk online casinos", "best casino sites uk", "best casinos",
            "top online casinos", "top 100 online casinos uk", "casino websites", "top 10 online casinos",
            "best casino online uk", "top casino sites", "best uk casino sites", "top 10 casino sites",
            "online casino sites", "best uk casinos", "top casino online", "top uk casinos",
            "casinos online uk", "top casinos", "top 10 casino online uk", "online casino"
        ]

        naked_url_pattern = r'(?:http[s]?://|www\.)|(?:\.com|\.net|\.org|\.co|\.uk)$'

        branded_count = 0
        exact_match_count = 0
        naked_url_count = 0
        other_generic_count = 0

        for anchor in anchors_in_file:
            if anchor in branded_variants:
                branded_count += 1
            elif anchor in exact_match_anchors:
                exact_match_count += 1
            elif (pd.Series([anchor]).str.contains(naked_url_pattern, regex=True)[0] and ' ' not in anchor):
                naked_url_count += 1
            else:
                other_generic_count += 1

        result_df = pd.DataFrame({
            'File Name': [file_name],
            'Target URL': [target_url],
            'Branded': [branded_count],
            'Exact Match': [exact_match_count],
            'Naked URL': [naked_url_count],
            'Other Generic': [other_generic_count]
        })

        return result_df
    
    except Exception as e:
        st.error(f"⚠️ Error processing {file_name}: {e}")
        return None

# Streamlit UI
st.title("🔗 Anchor Categorizer Web App")
st.write("Upload one or more CSV files, and get a categorized anchor text analysis!")

uploaded_files = st.file_uploader("Upload CSV Files", type="csv", accept_multiple_files=True)

if uploaded_files:
    results_df = pd.DataFrame()
    
    progress_bar = st.progress(0)
    
    for i, uploaded_file in enumerate(uploaded_files):
        file_name = uploaded_file.name
        st.write(f"📂 Processing: {file_name}")
        
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"❌ Could not read {file_name}: {e}")
            continue
        
        result_df = categorize_anchors_df(df, file_name)
        
        if result_df is not None:
            results_df = pd.concat([results_df, result_df], ignore_index=True)
        
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    if not results_df.empty:
        st.success("✅ Analysis complete!")

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            results_df.to_excel(writer, index=False, sheet_name='Anchor Analysis')
        excel_data = output.getvalue()

        st.download_button(
            label="📥 Download Results as Excel",
            data=excel_data,
            file_name='combined_anchor_counts.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        st.dataframe(results_df)
    else:
        st.warning("⚠️ No valid data processed.")
else:
    st.info("Please upload CSV files to begin.")
