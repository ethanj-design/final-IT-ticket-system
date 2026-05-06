import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class Employee:
    email: str
    password: str
    name: str
    department: str
    role: str
    phone: str
    computer: str
    status: str = "active"
    
