import time
import os
import streamlit as st
from openai import OpenAI
from services.ticket_manager import TicketManager
from services.employee_manager import EmployeeManager
from data.ticket_store import TicketStore
from services.audit_manager import AuditManager
from data.audit_store import audit_store
from datetime import datetime


api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key) if api_key else None

def build_ai_prompt() -> str:
    return (
        "You are a helpful IT support assistant for an internal company ticketing system. "
        "Help employees troubleshoot common IT issues like printers, VPN, login problems, "
        "slow computers, software, and hardware. "
        "Guardrails: "
        "- Keep responses concise (2-4 sentences). "
        "- Give clear, numbered steps when troubleshooting. "
        "- If the issue sounds serious or you can't resolve it, tell the user to submit a ticket. "
        "- Stay focused on IT support topics only."
    )


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
                 employee_manager: EmployeeManager, audit_manager: AuditManager, audit_store: audit_store) -> None:
        self.ticket_manager = ticket_manager
        self.ticket_store = ticket_store
        self.employee_manager = employee_manager
        self.audit_manager = audit_manager
        self.audit_store = audit_store
    
    def main(self):
        st.markdown(f'## Welcome Back, {st.session_state['user']}!')
        tab1, tab2, tab3 = st.tabs(['Home', 'Manual Ticket', 'AI Assistant'])
    
        if "chat_history" not in st.session_state:
            st.session_state['chat_history'] = []
        
        with tab1:
            self.show_home_page()
        with tab2:
            self.show_ticket_form()
        with tab3:
            self.show_ai_assistant()
    

    def show_home_page(self):
        user_tickets = self.ticket_manager.get_tickets_by_submitee(st.session_state['user'])
        ticket = self.ticket_manager.get_by_id(st.session_state['opened_button'])
        audit = self.audit_manager.get_by_id(st.session_state['opened_button'])

        st.markdown("## Home Page")

        ccol1, ccol2, ccol3 = st.columns([1,1,1])

        unopened_counter = 0
        for i in user_tickets:
            if i["status"] == "New":
                unopened_counter +=1
        
        resolved_counter = 0
        for i in user_tickets:
            if i["resolvedTime"] != "N/A":
                resolved_counter +=1
        
        st.subheader("Selected Ticket: Audit Log")
        with st.container(border=True):
            h1,h2,h3,h4,h5 = st.columns([1,1,1,1,1])
            h1.write("Timestamp")
            h2.write("New Assignee")
            h3.write("New Status")
            h4.write("New Severity")
            h5.write("New Notes")
            
            for a in audit:
                h1.write(a["timestamp"])
                if a["assignee"] != "N/A":
                    h2.write(a["assignee"])
                if a["status"] != "N/A":
                    h3.write(a["status"])
                if a["severity"] != "N/A":
                    h4.write(a["severity"])
                h5.write(a["notes"])
        
        
        with ccol1:
            st.metric('Your Tickets', value = len(user_tickets))
        with ccol2:
            st.metric('Unresolved', value=unopened_counter)
        with ccol3:
            st.metric("Closed", value = resolved_counter)

        st.markdown("### Your Current Tickets")

        with st.container(border = True):
            h1, h2, h3, h4, h5, h6, h7 = st.columns([1, 1, 1, 1, 1, 1, 1])
            h1.write('ID')
            h2.write('Description')
            h3.write('Assignee')
            h4.write('Status')
            h5.write('Severity')
            h6.write('Notes')
            h7.write("View Log")

            for t in user_tickets:
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])
                col1.write(t['id'])
                col2.write(t['descriptionShort'])
                col3.write(t['assignee'])
                col4.write(t['status'])
                col5.write(t['severity'])
                col6.write(t['notes']) 
                with col7:
                    if st.button('View Log', type = 'primary',key = f'open_ticket_btn_{t['id']}'):
                            st.session_state['opened_button'] = t['id']
                            st.rerun()

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
            long_desc = st.text_area('Deeper description of the issue (Optional)', 
                                     key = 'long_desc_ticketform')
            error_desc = st.text_area('Error Message (If Applicable)', placeholder = 'Paste here',
                                      key = 'error_desc_ticketform')
            submit_btn = st.button('Submit Ticket', use_container_width = True)

        if submit_btn:
            with st.spinner('Submitting ticket...'):
                time.sleep(2)
                try:
                    employee = self.employee_manager.get_by_email(st.session_state['email'])
                    new_ticket = self.ticket_manager.add(
                        email = st.session_state['email'],
                        name = st.session_state['user'],
                        phone = employee['phone'],
                        department = employee['department'],
                        problem_type = ticket_device,
                        application = ticket_application,
                        short_desc = short_desc,
                        long_desc = long_desc,
                        error_desc = error_desc,
                        computer = employee['computer']
            
                    )

                    self.ticket_store.save(self.ticket_manager.all())
                    st.success(f'Ticket {new_ticket['id']} created successfully!')
                    time.sleep(2)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
                    time.sleep(2)
                    st.rerun()

    def show_ai_assistant(self):
        st.subheader("AI Assistant")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption('Try asking: My printer won\'t connect')
        with col2:
            if st.button('Clear Messages'):
                st.session_state['chat_history'] = []
                st.rerun()

        with st.container(border=True, height=250):
            for message in st.session_state['chat_history']:
                with st.chat_message(message['role']):
                    st.write(message['content'])

        user_input = st.chat_input('Ask a question...')
        if user_input:
            st.session_state['chat_history'].append({'role': 'user', 'content': user_input})
            with st.spinner('Thinking...'):
                response = self.get_ai_response(user_input)
                st.session_state['chat_history'].append({'role': 'assistant', 'content': response})
            st.rerun()
    
    def get_ai_response(self, user_input: str) -> str:
        # First, check preset responses for common IT issues
        lowered = user_input.lower()
        best_match = None
        best_score = 0
        for item in PRESET_RESPONSES:
            score = sum(1 for keyword in item['keywords'] if keyword in lowered)
            if score > best_score:
                best_score = score
                best_match = item['response']
        if best_match:
            return best_match

        # Fall back to OpenAI for anything not covered by presets
        if client is None:
            return "OpenAI API key not configured. Please submit a ticket and IT will follow up."

        try:
            messages = [{"role": "system", "content": build_ai_prompt()}]
            for msg in st.session_state['chat_history']:
                messages.append({"role": msg['role'], "content": msg['content']})

            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=messages,
                temperature=1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I'm having trouble reaching the AI right now. Please submit a ticket. (Error: {str(e)})"
