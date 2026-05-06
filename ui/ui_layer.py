import time
import streamlit as st

def _wait_rerun(seconds: int = 2) -> None:
    time.sleep(seconds)
    st.rerun()

def _show_error(message: str) -> None:
    pass