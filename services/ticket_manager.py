import time
from datetime import datetime
from typing import List, Dict, Optional

class TicketManager:
    def __init__(self, initial_tickets: List[Dict]) -> None:
        self.tickets = initial_tickets
    
    def all(self) -> List[Dict]:
        return list(self.tickets)
    
    def get_by_id(self, ticket_id: str) -> Optional[Dict]:
        for t in self.tickets:
            if t['id'] == ticket_id:
                return t
        return None
    
    def get_open_tickets(self) -> List[Dict]:
        return [t for t in self.tickets if t['status'] in ('New', 'Open')]
    
    def get_tickets_by_assignee(self, asignee_name: str) -> List[Dict]:
        return [t for t in self.tickets if t['assignee'] == asignee_name]
    
    def filter(self, assignee: str = "None", severity: str = "All", 
               department: str = "All", status: str = "All") -> List[Dict]:
         return [
            t for t in self.tickets
            if (assignee == "None" or t["assignee"] == assignee)
            and (severity == "All" or t["severity"] == severity)
            and (department == "All" or t["department"] == department.lower())
            and (status == "All" or t["status"] == status)
        ]
    
    def add(self, email: str, name: str, phone: str, department: str, 
            problem_type: str, application: str, short_desc: str,
            long_desc: str, error_desc: str, computer: str) -> Dict:
        if not short_desc.strip():
            raise ValueError('Short description is required.')
        ticket_id = f"TK-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        new_ticket = {
            "id": ticket_id,
            "email": email,
            "name": name,
            "phone": phone,
            "date": datetime.today().strftime('%Y-%m-%d'),
            "time": time.strftime('%H:%M:%S'),
            "department": department.lower(),
            "problemType": problem_type,
            "application": application,
            "descriptionShort": short_desc,
            "descriptionLong": long_desc or "N/A",
            "errorDescription": error_desc or "N/A",
            "assignee": "Unassigned",
            "status": "New",
            "severity": "Medium",
            "compNumber": computer,
            "openedTime": "N/A",
            "resolvedTime": "N/A" 
        }
        self.tickets.append(new_ticket)
        return new_ticket
    
    def update(self, ticket_id: str, assignee: str, status: str,
               severity: str) -> Optional[Dict]:
        for t in self.tickets:
            if t['id'] == ticket_id:
                t['assignee'] = assignee
                t['status'] = status
                t['severity'] = severity
                if status == "Resolved" and t['resolvedTime'] == 'N/A':
                    t['resolvedTime'] = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
                return t
        return None
    

        
                
