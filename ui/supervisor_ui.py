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
        pass