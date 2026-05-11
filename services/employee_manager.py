import uuid
from typing import Dict, List, Optional

class EmployeeManager:
    def __init__(self, initial_employees: List[Dict]) -> None:
        self.employees = initial_employees
        print(f"DEBUG: EmployeeManager initialized with {len(initial_employees)} employees")
        if initial_employees:
            print(f"DEBUG: first employee email = {initial_employees[0].get('email')!r}")

    def all(self) -> List[Dict]:
        return list(self.employees)
    
    def get_by_email(self, email: str) -> Optional[Dict]:
        print(f"DEBUG: get_by_email searching {len(self.employees)} employees for {email!r}")
        for e in self.employees:
            if e['email'] == email:
                return e
        return None
    
    def validate_login(self, email: str, password: str) -> Optional[Dict]:
        employee = self.get_by_email(email)
        print(f"DEBUG: lookup email={email!r}, found={employee}")
        if employee:
            print(f"DEBUG: stored pw={employee['password']!r}, entered pw={password!r}")
        if employee and employee['password'] == password:
            return employee
        return None
    
    def get_it_staff_names(self) -> List[str]:
        return [e['name'] for e in self.employees if e['department'] == "it"]
    
    def add(self, email: str, name: str, password: str, department: str,
            role: str, phone: str, computer: str) -> Dict:
        if not email.strip or name.strip():
            raise ValueError("Email and name are required.")
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        if self.get_by_email(email):
            raise ValueError("An employee with this email already exists.")
        
        formatted_phone = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        
        new_employee = {
            "employee_id": str(uuid.uuid4()),
            "email": email,
            "password": password,
            "phone": formatted_phone,
            "name": name,
            "department": department.lower(),
            "role": role.lower(),
            "computer": "PC_" + computer,
            "status": "active"
        }
        self.employees.append(new_employee)
        return new_employee
 


