"""
FastAPI CRM Contacts API
Assignment 5: Complete CRUD API for managing contacts

This API provides:
- GET /contacts - List all contacts with filtering & pagination
- GET /contacts/{id} - Get single contact
- POST /contacts - Create new contact
- PUT /contacts/{id} - Update existing contact
- DELETE /contacts/{id} - Delete contact

Features:
- Input validation
- Error handling (404, 409, 422)
- Filtering by company and search
- Pagination with limit and offset
- Sorting by multiple fields
- Duplicate email detection
"""

from fastapi import FastAPI, HTTPException, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import Optional, List
from datetime import datetime

# Import our modules (with fallback for missing pydantic features)
try:
    from models import ContactCreate, ContactUpdate, ContactResponse, ContactsListResponse, ErrorResponse
    PYDANTIC_AVAILABLE = True
except ImportError:
    # Fallback to basic dict-based models
    PYDANTIC_AVAILABLE = False

from database import ContactsDatabase

# Initialize FastAPI app
app = FastAPI(
    title="CRM Contacts API",
    description="A lightweight CRM backend to manage contacts for a sales team",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = ContactsDatabase()

# Dependency to get database instance
def get_db():
    return db

@app.on_event("startup")
async def startup_event():
    """Initialize database and add sample data"""
    print("Starting CRM Contacts API...")
    db.init_database()
    db.seed_sample_data()
    print("Database initialized with sample data")

# Custom exception handler for database integrity errors
@app.exception_handler(sqlite3.IntegrityError)
async def integrity_error_handler(request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": "Email already exists", "error_code": "DUPLICATE_EMAIL"}
    )

# Root endpoint
@app.get("/")
async def root():
    """API information endpoint"""
    return {
        "message": "CRM Contacts API",
        "version": "1.0.0",
        "endpoints": {
            "list_contacts": "GET /contacts",
            "get_contact": "GET /contacts/{id}",
            "create_contact": "POST /contacts",
            "update_contact": "PUT /contacts/{id}",
            "delete_contact": "DELETE /contacts/{id}"
        }
    }

# Input validation functions (since we might not have full pydantic)
def validate_contact_data(data: dict) -> dict:
    """Validate contact data"""
    errors = []
    
    # Validate required fields
    if not data.get('name') or not data['name'].strip():
        errors.append("Name is required and cannot be empty")
    
    if not data.get('email'):
        errors.append("Email is required")
    elif '@' not in data['email']:
        errors.append("Email must contain '@' symbol")
    
    if errors:
        raise HTTPException(status_code=422, detail=errors)
    
    # Clean and format data
    cleaned_data = {
        'name': data['name'].strip(),
        'email': data['email'].lower().strip(),
        'phone': data.get('phone', '').strip() if data.get('phone') else None,
        'company': data.get('company', '').strip() if data.get('company') else None
    }
    
    return cleaned_data

@app.get("/contacts")
async def get_contacts(
    company: Optional[str] = Query(None, description="Filter by company (case-insensitive exact match)"),
    search: Optional[str] = Query(None, description="Search in name or email (substring match)"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results (1-50)"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    sort_by: str = Query("id", description="Sort field: id, name, company, email, created_at"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
    db: ContactsDatabase = Depends(get_db)
):
    """
    Retrieve all contacts with optional filtering, pagination, and sorting.
    
    Query Parameters:
    - company: Filter by company name (case-insensitive exact match)
    - search: Search substring in name or email fields
    - limit: Maximum results per page (default 10, max 50)
    - offset: Number of results to skip (default 0)
    - sort_by: Field to sort by (id, name, company, email, created_at)
    - order: Sort order (asc or desc)
    """
    try:
        result = db.get_contacts(
            limit=limit,
            offset=offset,
            company=company,
            search=search,
            sort_by=sort_by,
            order=order
        )
        
        # Convert datetime strings to proper format for response
        for contact in result['data']:
            if contact.get('created_at'):
                try:
                    # Convert to ISO format if needed
                    contact['created_at'] = contact['created_at']
                except:
                    contact['created_at'] = datetime.now().isoformat()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/contacts/{contact_id}")
async def get_contact(
    contact_id: int = Path(..., gt=0, description="Contact ID"),
    db: ContactsDatabase = Depends(get_db)
):
    """
    Retrieve a single contact by ID.
    
    Path Parameters:
    - contact_id: Unique contact identifier
    """
    contact = db.get_contact_by_id(contact_id)
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return contact

@app.post("/contacts", status_code=201)
async def create_contact(
    contact_data: dict,
    db: ContactsDatabase = Depends(get_db)
):
    """
    Create a new contact.
    
    Request Body:
    - name: Person's full name (required)
    - email: Email address with @ symbol (required)
    - phone: Phone number (optional)
    - company: Company name (optional)
    """
    try:
        # Validate input data
        validated_data = validate_contact_data(contact_data)
        
        # Create contact
        new_contact = db.create_contact(validated_data)
        
        return new_contact
        
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists")
    except HTTPException:
        # Re-raise HTTPExceptions (validation errors)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.put("/contacts/{contact_id}")
async def update_contact(
    contact_data: dict,
    contact_id: int = Path(..., gt=0, description="Contact ID"),
    db: ContactsDatabase = Depends(get_db)
):
    """
    Update an existing contact.
    
    Path Parameters:
    - contact_id: Unique contact identifier
    
    Request Body:
    - name: Person's full name (required)
    - email: Email address with @ symbol (required)
    - phone: Phone number (optional)
    - company: Company name (optional)
    """
    try:
        # Validate input data
        validated_data = validate_contact_data(contact_data)
        
        # Update contact
        updated_contact = db.update_contact(contact_id, validated_data)
        
        if not updated_contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        return updated_contact
        
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists")
    except HTTPException:
        # Re-raise HTTPExceptions (validation errors)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.delete("/contacts/{contact_id}", status_code=204)
async def delete_contact(
    contact_id: int = Path(..., gt=0, description="Contact ID"),
    db: ContactsDatabase = Depends(get_db)
):
    """
    Delete a contact by ID.
    
    Path Parameters:
    - contact_id: Unique contact identifier
    """
    deleted = db.delete_contact(contact_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    # FastAPI automatically returns 204 No Content for None return with status_code=204

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
