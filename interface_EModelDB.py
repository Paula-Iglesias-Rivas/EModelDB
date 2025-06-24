import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO
import zipfile
import base64, pathlib
import markdown as md
import streamlit.components.v1 as components

LOGO_FILE = pathlib.Path(__file__).with_name("logo.png")

if LOGO_FILE.exists():
    base64_logo = base64.b64encode(LOGO_FILE.read_bytes()).decode()
else:
    base64_logo = ""  # fallback (no logo)

# This line must be placed before displaying any element in the app
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
        /* Sidebar width */
        [data-testid="stSidebar"] {min-width: 300px; max-width: 300px;}
        /* Sidebar font size */
        [data-testid="stSidebar"] * {font-size: 18px !important;}
        /* Main block padding */
        [data-testid="stAppViewContainer"] .main .block-container {padding-left: 1rem; padding-right: 1rem;}
        /* Global font size */
        html, body, [class*="css"]  {font-size: 18px;}
        /* Full-width table and font */
        .streamlit-table {width: 100% !important; font-size: 18px;}
        table td, table th {font-size: 18px !important;}
        /* Header font */
        .custom-header {font-size: 22px !important; font-weight: bold;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# ReadMe text (shown inside the modal)
# --------------------------------------------------

READ_ME = r"""
<div style="text-align:center; font-size:24px; font-weight:700; line-height:1.3;">
This section provides basic information for understanding the data included in the database and the usability of the graphical user interface
</div>

---
### Substitution (rate) and score matrices
Substitution rate matrices present instantaneous relative rates of change between amino acids. These matrices, together with the amino acid frequencies at equilibrium, are traditionally used to construct probability matrices required for likelihood-based phylogenetic reconstruction methods (Yang 2006). Each element of a substitution matrix is an instantaneous relative rate, and, at the bottom (after the matrix), the amino-acid frequencies at equilibrium are provided (some models consider them to improve the fit with real data).

Score matrices, by contrast, display observed substitution scores for amino-acid changes and are traditionally used for sequence-alignment algorithms (Henikoff 1996). Each element of a score matrix is thus a score that reflects how often the change between two amino acids is observed.

Both kinds of matrices describe the frequency of substitutions between amino-acid pairs, but in different contexts (instantaneous rate vs. absolute observations) and, consequently, have different applications. For further details on empirical substitution models of protein evolution see Thorne (2000); Thorne & Goldman (2003); Arenas (2015).

---
### Triangular and rectangular matrices
Triangular matrices are reversible (symmetric): the rate or score from amino acid i to j equals the rate or score from j to i. If the matrix is not reversible (asymmetric), the rate or score depends on the direction of the substitution.

---
### Order of amino acids in the substitution matrices and amino-acid frequencies
A well-established alphabetical order—popularised by PAML (Yang 1995, 1997)—is widely used by default:

```
Ala Arg Asn Asp Cys Gln Glu Gly His Ile Leu Lys Met Phe Pro Ser Thr Trp Tyr Val
A   R   N   D   C   Q   E   G   H   I   L   K   M   F   P   S   T   W   Y   V
```
Most models in the database follow this order. In any case, the specific amino acids order for each model is provided.

---
### Incorporating new models
To propose a new model, email **paula.iglesias.rivas@uvigo.es**. All submissions are reviewed and, if error-free, included.

---
### References  
- Arenas M. 2015. *Trends in substitution models of molecular evolution.* Front Genet 6:319.  
- Henikoff S. 1996. *Scores for sequence searches and alignments.* Curr Opin Struct Biol 6:353-360.  
- Thorne J.L. 2000. *Models of protein sequence evolution and their applications.* Curr Opin Genet Dev 10:602-605.  
- Thorne J.L., Goldman N. 2003. *Probabilistic models for the study of protein evolution.* In: Handbook of Statistical Genetics. Wiley. p. 209-226.  
- Yang Z. 2006. *Computational Molecular Evolution.* Oxford University Press.  
- Yang Z. 1995. *PAML, phylogenetic analysis by maximum likelihood.* Version 1.1. Pennsylvania State University.  
- Yang Z. 1997. *PAML: a program package for phylogenetic analysis by maximum likelihood.* Comput Appl Biosci 13:555-556.
"""
# --------------------------------------------------
# Session‑state helpers
# --------------------------------------------------

if "show_readme" not in st.session_state:
    st.session_state.show_readme = False

def _open_readme():
    st.session_state.show_readme = True

def _close_readme():
    st.session_state.show_readme = False
    
# SQLite database connection
def get_connection():
    return sqlite3.connect('models.db')

# Function to query the database and apply filters
def query_database(author, name_model, year, taxonomic_group, matrix_type, comments, sort_by):
    conn = get_connection()
    text_columns = {"Name", "Author", "TaxonomicGroup", "MatrixType"}
    query = """SELECT name as Name, author as Author, publication_date as PublicationDate, 
                      article as Article, taxonomic_group as TaxonomicGroup, matrix_type as MatrixType, 
                      comments as Comments
               FROM AMINOACID_SUBSTITUTION_MODELS
               WHERE 1=1"""
    conditions, params=[], []
    # Apply filters based on input fields
    if author:
        conditions.append("lower(author) LIKE ?")
        params.append(f'%{author.lower()}%')

    if name_model:
        conditions.append("lower(name) LIKE ?")
        params.append(name_model.lower() + '%')

    if year:
        conditions.append("publication_date LIKE ?")
        params.append(year + '%')

    if taxonomic_group:
        conditions.append("lower(taxonomic_group) LIKE ?")
        params.append(taxonomic_group.lower() + '%')

    if matrix_type:
        conditions.append("lower(matrix_type) LIKE ?")
        params.append(matrix_type.lower() + '%')

    if comments:
        conditions.append("lower(comments) LIKE ?")
        params.append(comments.lower() + '%')
    
    if conditions:
        query += " AND " + " AND ".join(conditions)

    if sort_by in text_columns:
        query += f' ORDER BY "{sort_by}" COLLATE NOCASE ASC'
    else:
        query += f' ORDER BY "{sort_by}" ASC'

    # Secure execution
    df = pd.read_sql_query(query, conn, params=params)
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

# -----------------------
# Clear Filters & ReadMe dropdown **side by side**
# -----------------------
col_clear, col_readme = st.sidebar.columns(2)

with col_clear:
    if st.button("Clear"):
        st.session_state.clear()
        # Lightly reload the page
        st.write("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)
        

# ── medidas del pop-over ────────────────────────────────────────────────
POP_WIDTH_PX  = 1500     # ancho máximo del texto
POP_HEIGHT_VH = 60       # 30 % de la altura de la ventana
PIXELS_PER_VH = 9         # 1 vh ≈ 9 px  (ajusta 8–10 según tu pantalla)

html_readme = md.markdown(READ_ME, extensions=["fenced_code", "tables"])

with col_readme.popover("ReadMe", use_container_width=True):
    components.html(
        f"""
        <!-- hoja de estilos GitHub-Markdown -->
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.1.0/github-markdown.min.css">

        <style>
          /* 1️⃣  el iframe completo se pinta de blanco  */
          html, body {{
              height:100%;          /* hace que .markdown-body pueda ocupar todo */
              margin:0;
              background:#fff;      /* elimina la franja gris */
          }}

          /* 2️⃣  el contenido ocupa todo el alto del iframe y desplaza si es largo */
          .markdown-body {{
              box-sizing:border-box;
              height:100%;          /* llena todo el iframe */
              max-width:{POP_WIDTH_PX}px;
              overflow-y:auto; overflow-x:hidden;
              padding:1.25rem;      /* margen interior uniforme */
          }}
        </style>

        <div class="markdown-body">
            {html_readme}
        </div>

        <script>
          /* scroll arriba cada vez que se abre */
          document.querySelector('.markdown-body').scrollTop = 0;
        </script>
        """,
        height=int(POP_HEIGHT_VH * PIXELS_PER_VH),   # 30 vh reales
        width =POP_WIDTH_PX,
        scrolling=False,
    )


# Query database & prepare results
# --------------------------------------------------

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

# --------------------------------------------------
# Main view – headers & table
# --------------------------------------------------

# --- Encabezado con logo + texto -------------------------------------------
LOGO_PX = 200

header_html = f"""
<div style='display:flex; align-items:center; gap:0.75rem;'>
  <img src="data:image/png;base64,{base64_logo}" width="{LOGO_PX}" style="flex-shrink:0;" />
  <div style='display:flex; flex-direction:column;'>
     <span style='font-size:2.2rem; font-weight:700; line-height:1;'>Database of Empirical Substitution Models of Protein Evolution</span>
  </div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)



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
    with st.expander(f"View {row['Name']} matrix"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT binary_matrix FROM SUBSTITUTION_MATRIX WHERE model_id = ?', (row['Name'],))
        matrix_data = cursor.fetchone()
        conn.close()
        if matrix_data and matrix_data[0]:
            content=matrix_data[0]
            st.code(content.expandtabs(4))
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


# Contact section
st.sidebar.title("Contact Us")
st.sidebar.write("If you have any issues, please contact us: [paula.iglesias.rivas@uvigo.es](mailto:paula.iglesias.rivas@uvigo.es)")
