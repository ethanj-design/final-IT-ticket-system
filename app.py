import streamlit as st
import json
import time
from datetime import datetime
from pathlib import Path
import uuid


logo_image = Path("logo_svg.svg")

# INITIALS ----------------------------------------------------------------------------------------------------------------

st.set_page_config(layout="wide")

assginee_list = ["None"]

# format phone numbers
def format_phone(number):
    
    number = str(number)
   
    if len(number) == 10 and number.isdigit():
        return f"{number[:3]}-{number[3:6]}-{number[6:]}"
    else:
        return number 

# functions for jsons
def wait_rerun():
    time.sleep(2)
    st.rerun()

def load_json(file_path):

    path = Path(file_path) 
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    return data 

def overwrite_json(file_path, data):
    path = Path(file_path)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4,default=str)
    return True

employees = load_json("employees.json")
tickets = load_json("tickets.json")

# add to assignees
for e in employees:
    if e["department"] == "it":
        assginee_list.append(e["name"])

# Set session state
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "role" not in st.session_state:
    st.session_state["role"] = "none"

if "user" not in st.session_state:
    st.session_state["user"] = "none"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# INITIALS ----------------------------------------------------------------------------------------------------------------



# TICKET CREATOR FORM -----------------------------------------------------------------------------------------------------
if st.session_state["role"] == "staff" or st.session_state["role"] == "partner" or st.session_state["role"] == "manager":

    st.markdown(f"### Welcome Back, {st.session_state['user']}")

    tab1, tab2 = st.tabs(["Form", "AI Assistant"])
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    with tab1:
        st.markdown("Ticket Creation Form")



        with st.container(border=False):

            st.text(f"{st.session_state["email"]}")

            tick1, tick2 = st.columns([1,1])

            with tick1:
                ticket_device = st.selectbox("Software/Hardware", ["Software", "Hardware"],key="type_selection_ticketform")
            with tick2:
                if ticket_device == "Software":
                    ticket_application = st.selectbox("Details", ["Office Apps", "Email/Outlook", "Web Browser", "VPN/Remote Access", "Login Issue", "Permissions/Access", "Other"], key="software_select_ticketform")
                else:
                    ticket_application = st.selectbox("Details", ["Laptop/Desktop", "Printer", "Monitor", "Keyboard/Mouse", "Docking Station", "Phone", "Other"], key="hardware_select_ticketform")
            
            short_desc = st.text_input("Short Description of the Problem (Required)", 
                                            placeholder="Ex: Printer won't print", key="short_desc_ticketform")
            long_desc = st.text_area("Deeper descripton of the issue (Optional)", key="long_desc_ticketform")
            error_desc = st.text_area("Error Message (If Applicable)", placeholder="Paste here.",key="error_desc_ticketform")
            ticket_submit_btn = st.button("Submit Ticket",use_container_width=True)


        if ticket_submit_btn:

            with st.spinner("Working on submitting..."):
                time.sleep(4)
                required_fields_ticket = [ticket_device, ticket_application, short_desc]

                if any(not field for field in required_fields_ticket):

                    st.error("Please input text for all required fields.")
                    wait_rerun()
                else:
                    ticket_id = f"TK-{datetime.now().strftime('%Y%m%d%H%M%S')}" # Unique ID generator.
                    ticket_date = datetime.today().strftime("%Y-%m-%d")
                    ticket_time = time.strftime("%H:%M:%S")

                    if not long_desc:
                        long_desc = "n/a"
                    if not error_desc:
                        error_desc = "n/a"

                for e in employees:
                    if e["email"] == st.session_state["email"]:
                        found_ticket_user = e
            
                tickets.append({

                    "id" : ticket_id,
                    "email" : st.session_state["email"],
                    "name" : st.session_state["user"],
                    "phone" : found_ticket_user["phone"],
                    "date" : ticket_date,
                    "time" : ticket_time,
                    "department" : found_ticket_user["department"],
                    "problemType" : ticket_device,
                    "application" : ticket_application,
                    "descriptionShort" : short_desc,
                    "descriptionLong" : long_desc,
                    "errorDescription" : error_desc,
                    "assignee" : "Unasaigned",
                    "status" : "New",
                    "severity" : "Unassigned",
                    "compNumber" : found_ticket_user["computer"],
                    "openedTime" : "N/A",
                    "resolvedTime": "N/A"
            }
            )
            overwrite_json("tickets.json", tickets)
            st.success(f"Ticket {ticket_id} created successfully!")
            wait_rerun()

    with tab2:
        st.subheader("AI Assistant")
        col11, col22 = st.columns([3, 1])
        with col11:
            st.caption("Try asking: My printer won't connect")
        with col22:
            if st.button("Clear Messages"):
                st.session_state["chat_history"] = []
                st.rerun()

        with st.container(border=True, height=250):
            for message in st.session_state["chat_history"]:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        user_input = st.chat_input("Ask a question....")
        if user_input:
            with st.spinner("Thinking..."):
                st.session_state["chat_history"].append({"role": "user", "content": user_input})
                ai_respone = "I am working on it."

                # response is generated by ai
                st.session_state["chat_history"].append(
                        {
                            "role": "assistant",
                            "content": ai_respone
                        }
                    )
                time.sleep(2)
                st.rerun()
                
                

# TICKET SECTION -----------------------------------------------------------------------------------------------------------




# SUPERVISOR VIEWS ---------------------------------------------------------------------------------------------------------

# KPIS + SEARCH ------------------------------------------------------------------------------------------------------------

if st.session_state["role"] == "supervisor" and not st.session_state["page"] == "supervisor_make_acct":

    with st.container(border=False,width="stretch"):

        search1, search2, search3, search4 = st.columns([1,1,1,1,])

        with search1:
            search_assignee = st.selectbox("Assignee", assginee_list,key="search_assignee")
        with search2:
            search_severity = st.selectbox("Severity", ["All", "Low", "Medium", "High", "Severe"],key="search_severity")
        with search3: 
            search_department = st.selectbox("Department", ["All", "Accounting", "Marketing", "IT", "PMO Office"],key="search_department")
        with search4:
            search_status = st.selectbox("Status", ["All", "New", "Open", "Resolved"],key="search_status")

    filtered_tickets = [
        t for t in tickets
        if (search_assignee == "None" or t["assignee"] == search_assignee)
        and (search_severity == "All" or t["severity"] == search_severity)
        and (search_department == "All" or t["department"] == search_department.lower())
        and (search_status == "All" or t["status"] == search_status)
    ]

    st.write(f"{len(filtered_tickets)} ticket(s) found")

    with st.container(border=True):

        h1, h2, h3, h4, h5, h6, h7 = st.columns([1,1,1,1,1,1,1])
        h1.write("ID")
        h2.write("Description")
        h3.write("Assignee")
        h4.write("Email")
        h5.write("Status")
        h6.write("Severity")
        h7.write("")

        if not filtered_tickets:
            st.info("No tickets match your filters.")

        for t in filtered_tickets:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1,1,1,1,1,1,1])

            with col1:
                st.write(t['id'])

            with col2:
                st.write(t["descriptionShort"])

            with col3:
                st.write(t["assignee"])

            with col4:
                st.write(t["email"])

            with col5:
                st.write(t["status"])

            with col6:
                st.write(t["severity"])

            with col7:
                if st.button("Open Ticket", key=f"open_{t['id']}"):
                    st.session_state["selected_ticket"] = t
                    st.session_state["view"] = "ticket_detail"
                    st.rerun()

#CREATE A NEW PROFILE ------------------------------------------------------------------------------------------------------
if st.session_state["role"] == "supervisor" and st.session_state["page"] == "supervisor_make_acct":

 
    st.markdown(f"### Welcome Back, {st.session_state['user']}")

    with st.container(border=False):

        new_email = st.text_input("Create email address", placeholder="Ex: abc@fakecorp.com", key="new_email")
        new_name = st.text_input("Enter name", key="new_name")
        new_password = st.text_input("Enter password", key="new_pass", type="password")
        
        department1, department2 = st.columns([1,1])

        with department1:
            new_department = st.selectbox("Select Department", ["Accounting", "Marketing", "IT", "PMO Office"], key="dept_select")
        
        with department2:
            if new_department == "Accounting":
                new_role = st.selectbox("Select a role", ["Staff", "Partner"])
            elif new_department == "Marketing":
                new_role = st.selectbox("Select a role", ["Staff", "Manager"])
            elif new_department == "IT":
                new_role = st.selectbox("Select a role", ["Analyst", "Supervisor"])
            else:
                new_role = st.selectbox("Select a role", ["Staff", "Manager"])
        
        new_phone = st.text_input("Enter phone number", key="new_phone",placeholder="Ex: 1234567890 (do NOT use () or '-')")
        new_comp = st.text_input("Enter computer number", key="new_comp", placeholder="Ex: 0001")
        
        create_btn = st.button("Create Account", type="primary", use_container_width=True)

        if create_btn:

            with st.spinner("Creating account..."):
                time.sleep(5)
                failed = False
                required_fields = [new_email, new_name, new_password, new_department, new_role, new_phone, new_comp]

                if any(not field for field in required_fields):
                    st.warning("Please fill in all required fields!")
                    failed = True
                    wait_rerun()
                
                if len(new_phone) != 10:
                    st.error("Invalid phone number.")
                    failed = True
                    wait_rerun()
                
                for e in employees:
                    if e["email"] == new_email:
                        failed = True
                        st.error("Email already exists!")
                        wait_rerun()

                if not failed:
                    employees.append({
                        "employee_id": str(uuid.uuid4()),
                        "email": new_email,
                        "password": new_password,
                        "phone": format_phone(new_phone),
                        "name": new_name,
                        "department": new_department.lower(),
                        "role": new_role.lower(),
                        "computer": "PC_" + new_comp,
                        "status": "active"
                    })

                    overwrite_json("employees.json", employees)
                    st.success("Record created! User can now access TicketLive.")
                    time.sleep(3)
                    wait_rerun()

    #CREATE A NEW PROFILE END ---------------------------------------------------------------------------------------------------







# Login Page --------------------------------------------------------------------------------------------------------------------
if st.session_state["logged_in"] == False:

     # TicketLive Text
    

    # UI
    with st.container(border=False):


        col1, col2, col3, = st.columns([1,1,1])
        with col2:
            st.markdown("### Employee Login",text_alignment="center")

        login_email = st.text_input("Employee Email", placeholder="user@mct.com", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        login_btn = st.button("Login",type="primary",use_container_width=True)

        #CRUD Section
        if login_btn:

            found_user = "na"

            with st.spinner("Logging in..."):
                time.sleep(2)

                if not login_email or not login_password:
                    st.warning("Enter Required Information!")
                    wait_rerun()

                for e in employees:

                    if e["email"] == login_email and e["password"] == login_password:
                            found_user = e
                            break

                if found_user == e:
                    st.success(f"Welcome back, {found_user["name"]}")
                    st.session_state["email"] = found_user["email"]
                    st.session_state["user"] = found_user["name"]
                    st.session_state["role"] = found_user["role"]
                    st.session_state["logged_in"] = True
                    wait_rerun()
                else:
                    st.error("Invalid credentials!")
                    wait_rerun()
else:
    with st.sidebar:
        logout_btn = st.button("Logout")
    
        if logout_btn:
            with st.spinner("Logging out..."):
                time.sleep(2)
                st.session_state["logged_in"] = False
                st.session_state["page"] = "login"
                st.session_state["role"] = "none"
                st.session_state["user"] = "none"
                st.session_state["email"] = "none"
                
                st.success("Logged out!")
                wait_rerun()

        switch_view = st.button("Switch Supervisor View", type="primary")
        if switch_view:
            with st.spinner("Waiting..."):
                if st.session_state["page"] != "supervisor_make_acct":
                    st.session_state["page"] = "supervisor_make_acct"
                    wait_rerun()
                else:
                    st.session_state["page"] = "supervisor_main"
                    wait_rerun()
        
        if st.button("Ticket View"):
            st.session_state["role"] = "staff"
            wait_rerun()
        if st.button("Supervisor Views"):
            st.session_state["role"] = "supervisor"
            wait_rerun()