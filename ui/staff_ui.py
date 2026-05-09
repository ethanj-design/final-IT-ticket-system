import time
import streamlit as st
from services.ticket_manager import TicketManager
from services.employee_manager import EmployeeManager
from data.ticket_store import TicketStore


PRESET_RESPONSES = [
    {
        'keywords': ['printer', 'print', 'printing'],
        'response': 'Try restarting the printer and checking the connection.'
        ' Make sure it\'s set as your default printer.'
    },
     {
        "keywords": ["vpn", "remote", "access"],
        "response": "Make sure you're connected to the VPN. Try logging out and back in if the issue persists."
    },
    {
        "keywords": ["password", "login", "signin"],
        "response": "Try resetting your password or ensure caps lock is off."
    },
    {
        "keywords": ["slow", "lag", "performance"],
        "response": "Restart your computer and close unnecessary applications."
    }
    ]

class StaffUI:
    def __init__(self, ticket_manager: TicketManager, ticket_store: TicketStore,
                 employee_manager: EmployeeManager) -> None:
        self.ticket_manager = ticket_manager
        self.ticket_store = ticket_store
        self.employee_manager = employee_manager
    
    def main(self):
        st.markdown(f'## Welcome Back, {st.session_state['user']}!')
        tab1, tab2 = st.tabs(['Form'], ['AI Assistant'])
    
        if "chat_history" not in st.session_state:
            st.session_state['chat_history'] = []
        
        with tab1:
            self.show_ticket_form()
        with tab2:
            self.show_ai_assistant()
    
    def show_ticket_form(self):
        st.markdown('Ticket Creation Form')

        with st.container(border = False):
            st.text(st.session_state['email'])

            tick1, tick2 = st.columns([3, 1])
            with tick1:
                ticket_device = st.selectbox('Software/Hardware', ['Software', 'Hardware'],
                                             key = 'type_selection_ticketform')
            with tick2:
                if ticket_device == 'Software':
                    ticket_application = st.selectbox('Details', ['Office Apps', 'Email/Outlook', 'Web Browser', 'VPN/Remote Access',
                                                                  'Login Issue', 'Permission/Access', 'Other'],
                                                                   key = 'software_select_ticketform')
                else: 
                    ticket_application = st.selectbox('Details', ['Laptop/Desktop', 'Printer', 'Monitor', 'Keyboard/Mouse', 
                                                                  'Docking Station', 'Phone', 'Other'],
                                                                  key = 'hardware_select_ticketform')
            short_desc = st.text_input('Short Description of the Problem (Required)',
                                       placeholder = 'Ex: printer won\'t print', key = 'short_desc_ticketform')
            
