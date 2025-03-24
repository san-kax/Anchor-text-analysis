This **Streamlit** web application allows you to upload CSV files containing anchor text and target URLs.  
It analyzes the anchor texts and categorizes them into four types:

- **Branded**
- **Exact Match**
- **Naked URL**
- **Other Generic**

You can upload multiple CSV files and download the combined categorized results as an Excel file.

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) - Web app framework
- [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis
- [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) - Excel file handling
- [Tqdm](https://tqdm.github.io/) - Progress bars

- ## 📂 Input CSV Format

Your CSV files **must** contain at least the following columns:
- `Anchor`
- `Target URL`

Each file will be analyzed based on these two columns.

### Example CSV:

| Anchor             | Target URL             |
|--------------------|------------------------|
| best online casino | https://example.com/   |
| example.com        | https://example.com/   |
