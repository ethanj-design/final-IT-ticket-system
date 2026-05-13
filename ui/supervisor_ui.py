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
        st.markdown(f'### Welcome Back, {st.session_state['user']}!")

        if st.session_state['page'] == 'supervisor_main':
            self.show_dashboard()
        elif st.session_state['page'] == 'open_ticket':
            self.show_ticket_detail()
        elif st.session_state['page'] == 'supervisor_make_acct':
            self.show_create_account()

    def show_dashboard(self):
        open_tickets = self.ticket_manager.get_open_tickets()
        user_tickets = self.ticket_manager.get_tickets_by_assignee(st.session_state['user'])

        metric1, metric2, metric3, metric4 = st.columns([1, 1, 1, 1])
        with metric1:
            st.metric('Number of Open Tickets', value = len(open_tickets))
        with metric2:
            st.metric('Your Tickets', value = len(user_tickets))
        with metric3:
            st.metric('Average Resolve Time', value = 0)
        with metric4:
            st.metric('Average First-Open Time', value = 0)
        st.divider()

        search1, search2, search3, search4 = st.columns([1, 1, 1, 1])
        with search1:
            search_assignee = st.selectbox('Assignee', self.assignee_list,
                                           key = 'search_assignee')
        with search2:
            search_severity = st.selectbox('Severity', ['All', 'Low', 'Medium', 'High', 'Severe'],
                                           key = 'search_severity')
        with search3:
            search_department = st.selectbox('Department', ['All', 'Accounting', 'Marketing', 'IT', 'PMO Office'],
                                             key = 'search_department')
        with search4:
            search_status = st.selectbox('Status', ['All', 'New', 'Open', 'Resolved'], 
                                         key = 'search_status')
        filtered = self.ticket_manager.filter(
            assignee = search_assignee,
            severity = search_severity,
            department = search_department,
            status = search_status
        )

        st.write(f"{len(filtered)} ticket(s) found.")

        with st.container(border = True):
            h1, h2, h3, h4, h5, h6, h7 = st.columns([1, 1, 1, 1, 1, 1, 1])
            h1.write('ID')
            h2.write('Description')
            h3.write('Assignee')
            h4.write('Email')
            h5.write('Status')
            h6.write('Severity')
            h7.write('')

            if not filtered:
                st.info('No tickets match your filters.')
            for t in filtered:
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])
                col1.write(t['id'])
                col2.write(t['descriptionShort'])
                col3.write(t['assignee'])
                col4.write(t['email'])
                col5.write(t['status'])
                col6.write(t['severity'])
                with col7:
                    if st.button('Open Ticket', type = 'primary', key = f'open_ticket_btn_{t['id']}'):
                        st.session_state['opened_button'] = t['id']
                        st.session_state['page'] = 'open_ticket'
                        time.sleep(2)
                        st.rerun()
    
    def show_ticket_detail(self):
        ticket = self.ticket_manager.get_by_id(st.session_state['opened_button'])
        if not ticket:
            st.error('Ticket not found.')
            return
        
        st.title(f'Ticket: {ticket["id"]}')

        st.subheader('User Info')
        col1, col2 = st.columns(2)
        with col1:
            st.text_input('Name', ticket['name'], disabled = True)
            st.text_input('Email', ticket['email'], disabled = True)
        with col2:
            st.text_input('Phone', ticket['phone'], disabled= True)
            st.text_input('Department', ticket['department'], disabled = True)

        st.subheader('Issue Details')
        st.text_input('Problem Type', ticket['problemType'], disabled = True)
        st.text_area('Description', ticket['descriptionShort'], disabled = True)
        st.text_area('Description (more)', ticket['descriptionLong'], disabled = True)

        st.subheader('Update Ticket')
        assignee = st.selectbox('Assignee', self.assignee_list)
        status = st.selectbox("Status", ["All", "New", "Open", "Resolved"])
        severity = st.selectbox("Severity", ["Unassigned", "Low", "Medium", "High", "Critical"])

        if st.button('Save Changes'):
            self.ticket_manager.update(ticket['id'], assignee, status, severity)
            self.ticket_store.save(self.ticket_manager.all())
            st.success('Ticket updated successfully!')
            time.sleep(2)
            st.rerun()
        
        if st.button("Exit Ticket"):
            st.session_state['page'] = 'supervisor_main'
            st.rerun()

    def show_create_account(self):
        st.markdown('Create a New User')

        with st.container(border=False):
            new_email = st.text_input('Create email address', placeholder='Ex: abc@fakecorp.com',
                                    key='new_email')
            new_name = st.text_input('Enter name', key='new_name')
            new_password = st.text_input('Enter password', key='new_pass', type='password')

            dept_col, role_col = st.columns([1, 1])
            with dept_col:
                new_department = st.selectbox('Select Department',
                                            ['Accounting', 'Marketing', 'IT', 'PMO Office'],
                                            key='dept_select')
            with role_col:
                role_options = {
                    'Accounting': ['Staff', 'Partner'],
                    'Marketing': ['Staff', 'Manager'],
                    'IT': ['Analyst', 'Supervisor'],
                    'PMO Office': ['Staff', 'Manager']
                }
                new_role = st.selectbox('Select a role', role_options[new_department])

            new_phone = st.text_input('Enter phone number', key='new_phone',
                                    placeholder="Ex: 1234567890 (do NOT use () or '-')")
            new_comp = st.text_input('Enter computer number', key='new_comp', placeholder='Ex: 0001')

            create_btn = st.button('Create Account', type='primary', use_container_width=True)

            if create_btn:
                with st.spinner('Creating account...'):
                    time.sleep(5)
                    try:
                        self.employee_manager.add(
                            email=new_email,
                            name=new_name,
                            password=new_password,
                            department=new_department,
                            role=new_role,
                            phone=new_phone,
                            computer=new_comp
                        )
                        self.employee_store.save(self.employee_manager.all())
                        st.success('Record created!')
                        time.sleep(3)
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
                        time.sleep(2)
                        st.rerun()
