"""
Database models and schema for CRM Contacts API
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    """Base contact model with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Person's full name")
    email: str = Field(..., description="Email address (must contain @)")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number (optional)")
    company: Optional[str] = Field(None, max_length=100, description="Company name (optional)")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    @validator('email')
    def email_must_contain_at(cls, v):
        if '@' not in v:
            raise ValueError('Email must contain "@" symbol')
        return v.lower().strip()

    @validator('phone')
    def validate_phone(cls, v):
        if v is not None:
            return v.strip()
        return v

    @validator('company')
    def validate_company(cls, v):
        if v is not None:
            return v.strip()
        return v

class ContactCreate(ContactBase):
    """Model for creating a new contact"""
    pass

class ContactUpdate(ContactBase):
    """Model for updating an existing contact"""
    pass

class ContactResponse(ContactBase):
    """Model for contact response with additional fields"""
    id: int = Field(..., description="Unique contact ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True

class ContactsListResponse(BaseModel):
    """Model for paginated contacts list response"""
    data: list[ContactResponse]
    count: int = Field(..., description="Total number of contacts matching criteria")
    limit: int = Field(..., description="Maximum number of results per page")
    offset: int = Field(..., description="Number of results skipped")

class ErrorResponse(BaseModel):
    """Model for error responses"""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")

class SuccessResponse(BaseModel):
    """Model for success responses"""
    message: str = Field(..., description="Success message")
    data: Optional[dict] = Field(None, description="Additional data")
