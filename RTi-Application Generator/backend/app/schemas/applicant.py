"""
Pydantic Schemas - Applicant
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class ApplicantBase(BaseModel):
    """Base applicant information"""
    name: str
    address: str
    state: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class ApplicantCreate(ApplicantBase):
    """Applicant data for creating documents"""
    pass


class ApplicantInDocument(ApplicantBase):
    """Applicant data as it appears in documents"""
    formatted_address: Optional[str] = None
    
    def get_formatted_address(self) -> str:
        """Format address for document"""
        parts = [self.name, self.address, self.state]
        if self.phone:
            parts.append(f"Phone: {self.phone}")
        if self.email:
            parts.append(f"Email: {self.email}")
        return "\n".join(parts)
