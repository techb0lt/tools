import streamlit as st
import streamlit_book as stb

# Set wide display
st.set_page_config(
    layout="wide",
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        css-1uh038d {display: none}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
        
footer="""

<style> 
footer {visibility: hidden;}
footer:after {
	content: 'HP Inc.'; 
	visibility: visible;
	display: block;
	position: relative;
	#background-color: red;
	padding: 5px;
	top: 2px;
}
</style>
"""
st.markdown(footer, unsafe_allow_html=True)


stb.set_book_config(
        menu_title="TOOLS",
        menu_icon="private",
        options=[
            "Set Comparison",
            ], 
        paths=[
            "public/SetComparison.py", 
            ],
        save_answers=False,
        styles={
            "nav-link": {"--hover-color": "#e9f6fb"},
            "nav-link-selected": {"background-color": "#87CEEB"},
        }
        )        
