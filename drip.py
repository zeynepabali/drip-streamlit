import streamlit as st
import pandas as pd
import numpy as np
from stmol import showmol, render_pdb
import py3Dmol
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(layout="wide")
st.title("PDB Entries")

proteins_df = pd.read_csv('data/proteins_table.csv')
interfaces_df = pd.read_csv('data/interfaces_table.csv')
ligands_df = pd.read_csv('data/ligands_table.csv')


with st.sidebar:
    pdb_selection = st.multiselect("Filter by PDB ID", proteins_df.pdbID)

if len(pdb_selection) > 0:
    proteins_df = proteins_df[proteins_df.pdbID.isin(pdb_selection)]


int_builder = GridOptionsBuilder.from_dataframe(proteins_df[["pdbID", "interface_str", "ligand_str", "num_interfaces", "num_ligands", "fda"]])
int_builder.configure_default_column(editable=False, filterable=False, cellStyle={'text-align': 'center'})
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
                        fit_columns_on_grid_load=True)
