import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO
import zipfile

# This line must be placed before displaying any element in the app
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        /* Adjust the sidebar */
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }
        /* Adjust font size inside the sidebar */
        [data-testid="stSidebar"] * {
            font-size: 18px !important;
        }
        /* Ensure the main block does not have large margins */
        [data-testid="stAppViewContainer"] .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        /* Adjust global font size */
        html, body, [class*="css"]  {
            font-size: 18px; /* Adjust font size here */
        }

        /* Ensure the table spans full width and adjust font size */
        .streamlit-table {
            width: 100% !important;
            font-size: 18px; /* Adjust table font size */
        }
        
        /* Adjust font size in table cells */
        table td, table th {
            font-size: 18px !important;
        }

        /* Adjust font size of custom headers */
        .custom-header {
            font-size: 22px !important; /* Slightly larger header */
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


# SQLite database connection
def get_connection():
    return sqlite3.connect('models.db')

# Function to query the database and apply filters
def query_database(author, name_model, year, taxonomic_group, matrix_type, comments, sort_by):
    conn = get_connection()
    query = """SELECT name as Name, author as Author, publication_date as PublicationDate, 
                      article as Article, taxonomic_group as TaxonomicGroup, matrix_type as MatrixType, 
                      comments as Comments
               FROM AMINOACID_SUBSTITUTION_MODELS
               WHERE 1=1"""
    
    # Apply filters based on input fields
    if author:
        query += f" AND lower(author) LIKE '%{author.lower()}%'"
    if name_model:
        query += f" AND lower(name) LIKE '%{name_model.lower()}%'"
    if year:
        query += f" AND publication_date LIKE '{year}%'"
    if taxonomic_group:
        query += f" AND lower(taxonomic_group) LIKE '%{taxonomic_group.lower()}%'"
    if matrix_type:
        query += f" AND lower(matrix_type) LIKE '%{matrix_type.lower()}%'"
    if comments:
        query += f" AND lower(comments) LIKE '%{comments.lower()}%'"
    
    # Sort results based on the selected field
    query += f' ORDER BY "{sort_by}" ASC'

    # Execute query
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to get taxonomic group options from the database
def get_taxonomic_group_options():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT taxonomic_group FROM AMINOACID_SUBSTITUTION_MODELS')
    taxonomic_group_options = [row[0] for row in cursor.fetchall()]
    conn.close()
    taxonomic_group_options.insert(0, "")  # Empty option to allow searches without a filter
    return taxonomic_group_options

# Function to get matrix type options from the database
def get_matrix_type_options():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT matrix_type FROM AMINOACID_SUBSTITUTION_MODELS')
    matrix_type_options = [row[0] for row in cursor.fetchall()]
    conn.close()
    matrix_type_options.insert(0, "")  # Empty option to allow searches without a filter
    return matrix_type_options

# Function to download selected matrices into a ZIP file
def download_matrices(selected_models):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create an in-memory ZIP file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for model in selected_models:
            cursor.execute('SELECT binary_matrix FROM SUBSTITUTION_MATRIX WHERE model_id = ?', (model,))
            matrix_data = cursor.fetchone()
            if matrix_data:
                # Add the matrix to the ZIP
                zipf.writestr(f"{model}_matrix.txt", matrix_data[0])

    zip_buffer.seek(0)
    conn.close()
    return zip_buffer

# Sidebar with filters
st.sidebar.title("Filters")

# Filters
matrix_type = st.sidebar.selectbox("Matrix Type", options=get_matrix_type_options())
taxonomic_group = st.sidebar.selectbox("Taxonomic Group", options=get_taxonomic_group_options())
name_model = st.sidebar.text_input("Model Name")
author = st.sidebar.text_input("Author/s")
year = st.sidebar.text_input("Publication Year")
comments = st.sidebar.text_input("Comments")

# Sort by (use names without spaces here)
sort_by = st.sidebar.selectbox("Sort by", options=["Name", "Author", "PublicationDate", "TaxonomicGroup", "MatrixType"])

# Query database with filters
df_results = query_database(author, name_model, year, taxonomic_group, matrix_type, comments, sort_by)

# Modify the article column to include author, date, and link
df_results['References'] = df_results.apply(
    lambda row: f'<a href="{row["Article"]}">{row["Author"]} ({row["PublicationDate"]})</a>', axis=1
)

# Drop the Author and PublicationDate columns after creating the References column
df_results.drop(columns=['Author', 'PublicationDate', 'Article'], inplace=True)

# Reorder columns
df_results = df_results[['Name', 'MatrixType', 'TaxonomicGroup', 'Comments', 'References']]

# Add selection checkboxes for each row manually using a dictionary
selected_rows = {row['Name']: False for i, row in df_results.iterrows()}

# Add headers manually with the names of each column
st.write("# EModelDB")
st.write("### Database of Empirical Substitution Models of Protein Evolution")

# Display headers
header_cols = st.columns([2, 4, 4, 5, 5, 4])  # Adjust column widths
header_cols[0].markdown("<div class='custom-header'>Select</div>", unsafe_allow_html=True)
header_cols[1].markdown("<div class='custom-header'>Name</div>", unsafe_allow_html=True)
header_cols[2].markdown("<div class='custom-header'>Matrix Type</div>", unsafe_allow_html=True)
header_cols[3].markdown("<div class='custom-header'>Taxonomic Group</div>", unsafe_allow_html=True)
header_cols[4].markdown("<div class='custom-header'>Comments</div>", unsafe_allow_html=True)
header_cols[5].markdown("<div class='custom-header'>References</div>", unsafe_allow_html=True)


# Display table row by row with aligned elements
for i, row in df_results.iterrows():
    cols = st.columns([2, 4, 4, 5, 5, 4])  # Adjust column widths
    selected_rows[row['Name']] = cols[0].checkbox(
        "Seleccionar este modelo",  
        key=f"select_{i}",
        value=selected_rows[row['Name']],
        label_visibility="collapsed"  
    )
    cols[1].write(row['Name'])
    cols[2].write(row['MatrixType'])
    cols[3].write(row['TaxonomicGroup'])
    cols[4].write(row['Comments'])
    cols[5].markdown(row['References'], unsafe_allow_html=True)
    with st.expander(f"View matrix for {row['Name']} model"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT binary_matrix FROM SUBSTITUTION_MATRIX WHERE model_id = ?', (row['Name'],))
        matrix_data = cursor.fetchone()
        conn.close()
        if matrix_data and matrix_data[0]:
            st.text(matrix_data[0])
        else:
            st.warning(f"No matrix file found for {row['Name']} model")


# "Select All" button to select all rows (place it at the end)
select_all = st.checkbox("Select All", value=False)

# If "Select All" is checked, select all rows
if select_all:
    for name in selected_rows.keys():
        selected_rows[name] = True

# Create a list with the selected models
selected_models = [name for name, selected in selected_rows.items() if selected]

# Show download button if models are selected
if selected_models:
    zip_data = download_matrices(selected_models)
    st.download_button(
        label="Download Selected Matrices as ZIP",
        data=zip_data,
        file_name="matrices_selected.zip",
        mime="application/zip"
    )


# Clear filters
if st.sidebar.button("Clear Filters"):
    st.session_state.clear()  # Clear all session_state values
    st.write('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)  # Lightly reload the page


# Contact section
st.sidebar.title("Contact Us")
st.sidebar.write("If you have any issues, please contact us: [paula.iglesias.rivas@uvigo.es](mailto:paula.iglesias.rivas@uvigo.es)")
