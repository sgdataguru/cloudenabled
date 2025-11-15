"""
Database operations for CRM Contacts API
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

class ContactsDatabase:
    """Database class for managing contacts"""
    
    def __init__(self, db_path: str = "contacts.db"):
        """Initialize database connection and create table if not exists"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the contacts table if it doesn't exist"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    company TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    @contextmanager
    def get_db_connection(self):
        """Get database connection with automatic cleanup"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()
    
    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new contact
        
        Args:
            contact_data: Dictionary with contact information
            
        Returns:
            Dictionary with created contact including ID
            
        Raises:
            sqlite3.IntegrityError: If email already exists
        """
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check for duplicate email
            cursor.execute("SELECT id FROM contacts WHERE email = ?", (contact_data['email'],))
            if cursor.fetchone():
                raise sqlite3.IntegrityError("Email already exists")
            
            # Insert new contact
            cursor.execute("""
                INSERT INTO contacts (name, email, phone, company, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                contact_data['name'],
                contact_data['email'],
                contact_data.get('phone'),
                contact_data.get('company'),
                datetime.now().isoformat()
            ))
            
            contact_id = cursor.lastrowid
            conn.commit()
            
            # Return the created contact
            return self.get_contact_by_id(contact_id)
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Dict[str, Any]]:
        """Get a contact by ID"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def get_contacts(self, 
                    limit: int = 10, 
                    offset: int = 0, 
                    company: Optional[str] = None, 
                    search: Optional[str] = None,
                    sort_by: str = "id",
                    order: str = "asc") -> Dict[str, Any]:
        """
        Get contacts with filtering, pagination, and sorting
        
        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            company: Filter by company (case-insensitive exact match)
            search: Search in name or email (substring match)
            sort_by: Sort field (name, company, id)
            order: Sort order (asc, desc)
            
        Returns:
            Dictionary with data, count, limit, offset
        """
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build WHERE clause
            where_conditions = []
            params = []
            
            if company:
                where_conditions.append("LOWER(company) = LOWER(?)")
                params.append(company)
            
            if search:
                where_conditions.append("(name LIKE ? OR email LIKE ?)")
                search_param = f"%{search}%"
                params.extend([search_param, search_param])
            
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            # Validate sort parameters
            valid_sort_fields = ["id", "name", "company", "email", "created_at"]
            if sort_by not in valid_sort_fields:
                sort_by = "id"
            
            if order.lower() not in ["asc", "desc"]:
                order = "asc"
            
            # Get total count
            count_query = f"SELECT COUNT(*) FROM contacts {where_clause}"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0]
            
            # Get paginated results
            order_clause = f"ORDER BY {sort_by} {order.upper()}"
            data_query = f"""
                SELECT * FROM contacts 
                {where_clause} 
                {order_clause} 
                LIMIT ? OFFSET ?
            """
            cursor.execute(data_query, params + [limit, offset])
            rows = cursor.fetchall()
            
            contacts = [dict(row) for row in rows]
            
            return {
                "data": contacts,
                "count": total_count,
                "limit": limit,
                "offset": offset
            }
    
    def update_contact(self, contact_id: int, contact_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing contact
        
        Args:
            contact_id: ID of contact to update
            contact_data: New contact data
            
        Returns:
            Updated contact data or None if not found
            
        Raises:
            sqlite3.IntegrityError: If email conflicts with another contact
        """
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if contact exists
            cursor.execute("SELECT id FROM contacts WHERE id = ?", (contact_id,))
            if not cursor.fetchone():
                return None
            
            # Check for duplicate email (excluding current contact)
            cursor.execute(
                "SELECT id FROM contacts WHERE email = ? AND id != ?", 
                (contact_data['email'], contact_id)
            )
            if cursor.fetchone():
                raise sqlite3.IntegrityError("Email already exists")
            
            # Update contact
            cursor.execute("""
                UPDATE contacts 
                SET name = ?, email = ?, phone = ?, company = ?
                WHERE id = ?
            """, (
                contact_data['name'],
                contact_data['email'],
                contact_data.get('phone'),
                contact_data.get('company'),
                contact_id
            ))
            
            conn.commit()
            
            # Return updated contact
            return self.get_contact_by_id(contact_id)
    
    def delete_contact(self, contact_id: int) -> bool:
        """
        Delete a contact by ID
        
        Args:
            contact_id: ID of contact to delete
            
        Returns:
            True if contact was deleted, False if not found
        """
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()
            
            return cursor.rowcount > 0
    
    def seed_sample_data(self):
        """Add sample data for testing"""
        sample_contacts = [
            {"name": "John Doe", "email": "john.doe@acme.com", "phone": "555-0101", "company": "Acme Corp"},
            {"name": "Jane Smith", "email": "jane.smith@techco.com", "phone": "555-0102", "company": "TechCo"},
            {"name": "Alice Johnson", "email": "alice.j@startupx.com", "phone": "555-0103", "company": "StartupX"},
            {"name": "Bob Wilson", "email": "bob.w@acme.com", "phone": "555-0104", "company": "Acme Corp"},
            {"name": "Carol Brown", "email": "carol.b@freelance.com", "phone": "555-0105", "company": None},
        ]
        
        for contact in sample_contacts:
            try:
                self.create_contact(contact)
            except sqlite3.IntegrityError:
                # Contact already exists, skip
                pass
