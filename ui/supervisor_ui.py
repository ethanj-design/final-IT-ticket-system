import time
import streamlit as st
from services.ticket_manager import TicketManager
from services.employee_manager import EmployeeManager
from data.ticket_store import TicketStore
from data.employee_store import EmployeeStore

ASSIGNEE_BASE = ['None', 'Unassigned']

class SupervisorUI:
    def __init__(self, ticket_manager: TicketManager, ticket_store: TicketStore,
                 employee_manager: EmployeeManager, employee_store: EmployeeStore) -> None:
        self.ticket_manager = ticket_manager
        self.ticket_store = ticket_store
        self.employee_manager = employee_manager
        self.employee_store = employee_store
        self.assignee_list = ASSIGNEE_BASE + self.employee_manager.get_it_staff_names()

    def main(self):
        st.markdown(f'### Welcome Back, {st.session_state['user']}!')

        if st.session_state['page'] == 'supervisor_main':
            self.show_dashboard()
        elif st.session_state['page'] == 'open_ticket':
            self.show_ticket_detail()
        elif st.session_state['page'] == 'supervisor_make_account':
            self.show_create_account()

    def show_dashboard(self):
        open_tickets = self.ticket_manager.get_open_tickets()
        user_tickets = self.ticket_manager.get_tickets_by_assignee(st.session_state['user'])

        metric1, metric2, metric3, metric4 = st.columns([1, 1, 1, 1])
        with metric1:
            st.metric('Number of Open Tickets', value = len(open_tickets))
        pass