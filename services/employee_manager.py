import uuid
from typing import Dict, List, Optional

class EmployeeManager:
    def __init__(self, initial_employees: List[Dict]) -> None:
        self.employees = initial_employees

    def all(self) -> List[Dict]:
        return list(self.employees)
    
    def get_by_email(self, email: str) -> Optional[Dict]:
        for e in self.employees:
            if e['email'] == email:
                return e
        return None
    
    def validate_login(self, email: str, password: str) -> Optional[Dict]:
        employee = self.get_by_email(email)
        if employee and employee['password'] == password:
            return employee
        return None
    
    def get_it_staff_names(self) -> List[str]:
        pass

