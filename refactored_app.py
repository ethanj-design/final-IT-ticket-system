import time
import streamlit as st
from pathlib import Path

from data.employee_store import EmployeeStore
from data.ticket_store import TicketStore
from services.employee_manager import EmployeeManager
from services.ticket_manager import TicketManager
from ui.login_ui import LoginUI
from ui.staff_ui import StaffUI
from ui.supervisor_ui import SupervisorUI

st.set_page_config(layout = 'wide')

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = 'none'
if 'user' not in st.session_state:
    st.session_state['user'] = 'none'
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'
if 'opened_button' not in st.session_state:
    st.session_state['opened_button'] = 'None'

employee_store = EmployeeStore(Path('employees.json'))
ticket_store = TicketStore(Path('tickets.json'))

employee_manager = EmployeeManager(employee_store.load())
ticket_manager = TicketManager(ticket_store.load())

if st.session_state['logged_in']:
    with st.sidebar:
        if st.button('Logout'):
            with st.spinner('Logging out...'):
                time.sleep(2)
                for key in ['logged_in', 'page', 'role', 'user', 'email']:
                    st.session_state[key] = False if key == 'logged_in' else 'none'
                st.session_state['page'] = 'login'
                st.success('Logged out!')
                time.sleep(2)
                st.rerun()

        if st.session_state['role'] == 'supervisor':
            
            if st.button('Switch Supervisor View', type = 'primary'):
                if st.session_state['page'] != 'supervisor_make_acct':
                    st.session_state['page'] = 'supervisor_make_acct'
                else:
                    st.session_state['page'] = 'supervisor_main'
                st.rerun()
            if st.button('Ticket View'):
                st.session_state['role'] = 'staff'
                st.rerun()
if not st.session_state['logged_in']:
    login_ui = LoginUI(employee_manager)
    login_ui.show()
elif st.session_state['role'] in ('staff', 'partner', 'manager'):
    staff_ui = StaffUI(ticket_manager, ticket_store, employee_manager)
    staff_ui.main()
elif st.session_state['role'] == 'supervisor':
    supervisor_ui = SupervisorUI(ticket_manager, ticket_store, employee_manager, employee_store)
    supervisor_ui.main()
