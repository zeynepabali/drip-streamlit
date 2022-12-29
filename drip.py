import streamlit as st
import pandas as pd
import numpy as np
from stmol import showmol, render_pdb
import py3Dmol
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(layout="wide")
st.title("Interface Dataset")

proteins_df = pd.read_csv('data/proteins_table.csv')
interfaces_df = pd.read_csv('data/interfaces_table.csv')
ligands_df = pd.read_csv('data/ligands_table.csv')

int_builder = GridOptionsBuilder.from_dataframe(proteins_df)
int_builder.configure_default_column(editable=False, filterable=False, cellStyle={'text-align': 'center'})
int_builder.configure_column("pdbID", header_name="Interface ID", editable=False, )
int_builder.configure_column("interface_id", header_name="Chain 1")
int_builder.configure_column("ligands", header_name="Chain 2")
int_builder.configure_column('fda_approved', header_name="# Chain 1")
int_builder.configure_column("num_interfaces", header_name="# Chain 2")
int_builder.configure_column("num_ligands", header_name="# Interface Residues")
int_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=int_select_pagination)
int_builder.configure_selection('single', use_checkbox=True)

with st.spinner('Loading data...'):
    int_return = AgGrid(proteins_df,
                        width='100%',
                        theme='material',
                        enable_enterprise_modules=False,
                        gridOptions=int_builder.build(),
                        fit_columns_on_grid_load=True)
