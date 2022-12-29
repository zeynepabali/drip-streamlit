import streamlit as st
import pandas as pd
import numpy as np
from stmol import showmol, render_pdb
import py3Dmol
from datetime import datetime
from PIL import Image
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(page_title="DiPPI", layout="wide")


proteins_df = pd.read_csv('data/proteins_table.csv')
interfaces_df = pd.read_csv('data/interfaces_table.csv')
ligands_df = pd.read_csv('data/ligands_table.csv')


col1, col2 = st.columns(2)

with col2:
    logo_image = Image.open("data/drip_image.jfif")
    st.image(logo_image, width=400)

with col1:
    st.title("DiPPI")

with st.sidebar:
    pdb_selection = st.multiselect("Filter by PDB ID", proteins_df.pdbID)
    ligand_selection = st.multiselect("Filter by ligand ID", ligands_df.ligands)

    if len(pdb_selection) > 0:
        proteins_df = proteins_df[proteins_df.pdbID.isin(pdb_selection)]


int_builder = GridOptionsBuilder.from_dataframe(proteins_df[["pdbID", "interface_str", "ligand_str", "num_interfaces", "num_ligands", "fda"]])
int_builder.configure_default_column(editable=False, filterable=True, cellStyle={'text-align': 'center'})
int_builder.configure_column("pdbID", header_name="PDB ID", editable=False, )
int_builder.configure_column("interface_str", header_name="Interfaces")
int_builder.configure_column("ligand_str", header_name="Ligands")
int_builder.configure_column('num_interfaces', header_name="# of Interfaces")
int_builder.configure_column("num_ligands", header_name="# of Ligands")
int_builder.configure_column("fda", header_name="FDA Approved")
int_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=20)

with st.spinner('Loading data...'):
    int_return = AgGrid(proteins_df,
                        width='100%',
                        theme='material',
                        enable_enterprise_modules=False,
                        gridOptions=int_builder.build(),
                        fit_columns_on_grid_load=True,
                        custom_css={".ag-header-cell-label": {"justify-content": "center;"}})
