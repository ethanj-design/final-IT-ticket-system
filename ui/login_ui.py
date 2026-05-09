import time
import streamlit as st
from services.employee_manager import EmployeeManager

class LoginUI:
    def __init__(self, employee_manager: EmployeeManager) -> None:
        self.manager = employee_manager
    
    def show(self):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown('## Employee Login')
        
        login_email = st.text_input('Employee Email', placeholder = 'user@mct.com',
                                    key = 'login_email')
        login_password = st.text_input('Password', type = 'password',
                                       key = 'login_password')
        login_btn = st.button('Login', type = 'primary', use_container_width = True)

        if login_btn:
            if not login_email or not login_password:
                st.warning('Please enter your email and password.')
                return
        
            with st.spinner('Logging in...'):
                time.sleep(2)
                found_user = self.manager.validate_login(login_email, login_password)

                if found_user:
                    st.success(f'Welcome back, {found_user['name']}!')
                    st.session_state['logged_in'] = True
                    st.session_state['email'] = found_user['email']
                    st.session_state['user'] = found_user['name']
                    st.session_state['role'] = found_user['role']
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error('Invalid credentials!')
                    time.sleep(2)
                    st.rerun()


