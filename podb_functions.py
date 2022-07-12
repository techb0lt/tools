# podb fucntions

import streamlit as st
import streamlit_book as stb
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import sqlite3 as sql
from pandas import ExcelWriter

#-----------------------------------
# Function to create sqlite tables #
#-----------------------------------


def to_sql(df_name, tbl_name):
    from sqlalchemy import create_engine
    import pandas as pd
    engine = create_engine('sqlite:///PODB.db', echo=False)
    engine.execute('DROP TABLE IF EXISTS ' + tbl_name)
    df_name.to_sql(tbl_name, con=engine)
    engine.dispose()

def run_sql(query):
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///PODB.db', echo=False)
    engine.execute(query)
    engine.dispose()    

def run_sql_file(query):
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///PODB.db', echo=False)
    engine.execute(query.read())
    engine.dispose() 

def read_sql(query,date_col_list=False):
    from sqlalchemy import create_engine
    import pandas as pd
    engine = create_engine('sqlite:///PODB.db', echo=False)
    df_name = pd.read_sql(query, con=engine,parse_dates=date_col_list).fillna('').convert_dtypes()
    engine.dispose()
    return df_name
    
#---------------------------
# Function to upload excel #
#---------------------------

def read_upload(obj_file,str_sheetname,col_list=None, date_col_list=False, file_type='xlsx'):
    import pandas as pd
    dataframe=""
    
    try:
        if obj_file is not None:
            if file_type == 'csv':
                dataframe = pd.read_csv(obj_file, usecols=col_list, parse_dates = date_col_list).applymap(lambda s: s.upper() if type(s) == str else s).fillna('')
            else:
                dataframe = pd.read_excel(obj_file,sheet_name = str_sheetname, usecols=col_list, parse_dates = date_col_list).applymap(lambda s: s.upper() if type(s) == str else s).fillna('')
            with st.expander(str_sheetname+" Sample", expanded=False):
                #st.markdown('**Sample of upload**')
                st.write(dataframe.head())
        else:
            dataframe="Empty - Upload a file first"
            st.warning(dataframe)			
    except ValueError as e:
        st.error("Problem: "+ e.args[0])
    finally:
        return dataframe


def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """    
    
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )
    options.configure_pagination(paginationAutoPageSize=True) #Add pagination
    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

def generic_aggrid(data: pd.DataFrame):
    gb = GridOptionsBuilder.from_dataframe(data, enableRowGroup=True, enableValue=True, enablePivot=True)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    #gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()
    
    grid_response = AgGrid(data,
    gridOptions=gridOptions,
    # enableRowGroup=True,
    # enableValue=True,
    # enablePivot=True,
    enable_enterprise_modules=True,
    theme="streamlit",
    allow_unsafe_jscode=True,
    reload_data=False,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=False
    )
    
    return grid_response
    