import time
from datetime import datetime
from typing import List, Dict, Optional
import uuid

class AuditManager:

    def __init__(self, initial_audits: List[Dict]) -> None:
        self.audit_log = initial_audits

    def all(self) -> List[Dict]:
        return list(self.audit_log)

    
    def get_by_id(self, ticket_id: str) -> List[Dict[str, Any]]:
        results = []
        for a in self.audit_log:
            if a.get('ticket_id') == ticket_id:
                results.append(a)
        return results

    def add(self, ticket_id: str, assignee: str, severity: str, status: str, notes: str):

        new_audit_entry = {
            "id" : str(uuid.uuid4()),
            "timestamp": datetime.now(),
            "ticket_id" : ticket_id,
            "assignee" : assignee,
            "severity" : severity,
            "status" : status,
            "notes" : notes
        }
        self.audit_log.append(new_audit_entry)
        return new_audit_entry
