# 📋 Complete Exam Solution Plan - Practical Assessment

## 📝 Overview
- **Total Duration**: 6 assignments
- **Technologies**: Python, Pandas/NumPy, TensorFlow, FastAPI, Flask
- **Focus Areas**: Data structures, file handling, data analysis, ML, web APIs, chatbots

## 🎯 Assignment Breakdown & Implementation Plan

### ✅ Assignment 1: Python Data & Control Practice (20 min)
**Status**: [ ] Not Started  
**Focus**: Variables, Data Types, Operators, Lists, Tuples, Dictionaries  
**Points**: 10 marks

**Requirements**:
- Ask user to enter five student names and their marks out of 100
- Store data in a dictionary (name → marks)
- Calculate and print:
  - The average mark
  - The name(s) of the student(s) with the highest mark
  - A sorted list of all students in alphabetical order
  - Display all students who scored above the average

**Implementation Tasks**:
- [ ] Create student data collection system
- [ ] Implement dictionary storage (name → marks)
- [ ] Calculate average marks
- [ ] Find top scorer(s)
- [ ] Sort students alphabetically
- [ ] Display above-average students

**Assessment Criteria**:
- Correct use of data structures (3 marks)
- Accurate calculations (3 marks)
- Proper output formatting (2 marks)
- Code readability and comments (2 marks)

---

### ✅ Assignment 2: File Handling & Functions (20 min)
**Status**: [ ] Not Started  
**Focus**: File Handling, Functions, Data Processing  
**Points**: 10 marks

**Requirements**:
- Read data from "sales.txt" (product_name, quantity_sold, price_per_unit)
- Define function calculate_total(quantity, price)
- Write results to "sales_summary.txt" showing:
  - Product name
  - Quantity sold
  - Total sales amount

**Implementation Tasks**:
- [ ] Create sample sales.txt file
- [ ] Implement file reading logic
- [ ] Define calculate_total() function
- [ ] Process each line and calculate totals
- [ ] Write formatted results to output file

**Assessment Criteria**:
- Correct file handling (3 marks)
- Functional decomposition (3 marks)
- Accurate calculations (2 marks)
- Output and readability (2 marks)

---

### ✅ Assignment 3: Data Analysis with Pandas & NumPy (20 min)
**Status**: [ ] Not Started  
**Focus**: NumPy, Pandas, Data Cleaning, Statistics  
**Points**: 10 marks

**Requirements**:
- Load students_scores.csv (Name, Math, Physics, Chemistry)
- Replace missing values (NaN) with column mean
- Using NumPy, calculate:
  - Overall average score for each student
  - Highest and lowest average score in class
- Create new 'Average' column and save to students_scores_updated.csv

**Implementation Tasks**:
- [ ] Create sample students_scores.csv
- [ ] Load data with Pandas
- [ ] Clean missing values (replace with mean)
- [ ] Implement NumPy calculations for averages
- [ ] Find min/max averages
- [ ] Update DataFrame and export to CSV

**Assessment Criteria**:
- Data loading and cleaning (3 marks)
- Correct calculations using NumPy (3 marks)
- Proper file output (2 marks)
- Code readability and comments (2 marks)

---

### ✅ Assignment 4: TensorFlow CNN Classification (20 min)
**Status**: [ ] Not Started  
**Focus**: TensorFlow, CNN, Image Classification  
**Points**: 10 marks

**Requirements**:
- Train CNN to classify Donald Trump vs Lawrence Wong images
- Data structure: data/train/ and data/val/ folders
- Use 20-50 images per class for training, 5-10 for validation
- Build & train model, evaluate on validation set
- Test prediction on uploaded image
- Write brief reflection (3-5 sentences)

**Implementation Tasks**:
- [ ] Set up data directory structure
- [ ] Prepare sample image datasets
- [ ] Build CNN architecture using TensorFlow/Keras
- [ ] Train model with validation split
- [ ] Evaluate accuracy and create confusion matrix
- [ ] Implement single image prediction
- [ ] Write reflection on model performance

**Assessment Criteria**:
- Data setup & loading (2 marks)
- Model & training (4 marks)
- Evaluation (2 marks)
- Prediction demo (2 marks)

---

### ✅ Assignment 5: FastAPI CRM Contacts API
**Status**: [ ] Not Started  
**Focus**: FastAPI, SQLite, CRUD Operations  
**Points**: 100 points

**Requirements**:
SQLite table 'contacts' with: id, name, email, phone, company

**Endpoints to implement**:
1. **GET /contacts** - List all contacts with filtering & pagination
2. **GET /contacts/{id}** - Get single contact
3. **POST /contacts** - Create new contact
4. **PUT /contacts/{id}** - Update existing contact
5. **DELETE /contacts/{id}** - Delete contact

**Implementation Tasks**:
- [ ] Design SQLite database schema
- [ ] Set up FastAPI application structure
- [ ] Implement all CRUD endpoints
- [ ] Add validation (email format, required fields)
- [ ] Implement filtering (company, search)
- [ ] Add pagination (limit, offset)
- [ ] Error handling (404, 409, 422)
- [ ] Bonus: Duplicate email check, sorting, timestamps

**Assessment Criteria**:
- CRUD endpoints implemented (40 points)
- Validation (20 points)
- Filtering + pagination (20 points)
- Error handling (10 points)
- Clean code & README (10 points)

---

### ✅ Assignment 6: Healthcare Assistant Chatbot (30 min)
**Status**: [ ] Not Started  
**Focus**: Flask, OpenAI LLM, Web Development  
**Points**: 10 points

**Requirements**:
- Flask web app with chat interface
- Routes: / (chat page), /chat (POST for responses)
- Knowledge base covering diet tips and health practices
- OpenAI LLM integration for responses
- Medical disclaimer and safety redirects
- Chat history (last 5 messages)

**Implementation Tasks**:
- [ ] Set up Flask application with routes
- [ ] Create HTML chat interface
- [ ] Implement knowledge base (diet plans, do's/don'ts)
- [ ] Integrate OpenAI API for intelligent responses
- [ ] Add medical disclaimers and safety guardrails
- [ ] Implement conversation history
- [ ] Test safety redirects for medical queries

**Assessment Criteria**:
- Routing & App structure (2 points)
- Chat logic (3 points)
- Knowledge coverage (2 points)
- UI/UX (2 points)
- Safety & style (1 point)

## 🛠️ Implementation Strategy

### Phase 1: Foundation (Python Basics)
1. **Assignment 1** - Python data structures and control flow
2. **Assignment 2** - File handling and functions

### Phase 2: Data Science
3. **Assignment 3** - Pandas/NumPy data analysis

### Phase 3: Web Development
4. **Assignment 5** - FastAPI REST API
5. **Assignment 6** - Flask chatbot with AI integration

### Phase 4: Machine Learning
6. **Assignment 4** - TensorFlow CNN (most complex, requires setup)

## 📁 Project Structure
```
exam-solutions/
├── README.md
├── IMPLEMENTATION_PLAN.md
├── assignment1/
│   └── student_marks.py
├── assignment2/
│   ├── file_handler.py
│   ├── sales.txt
│   └── sales_summary.txt
├── assignment3/
│   ├── data_analysis.py
│   ├── students_scores.csv
│   └── students_scores_updated.csv
├── assignment4/
│   ├── cnn_classifier.py
│   ├── requirements.txt
│   └── data/
│       ├── train/
│       │   ├── donald_trump/
│       │   └── lawrence_wong/
│       └── val/
│           ├── donald_trump/
│           └── lawrence_wong/
├── assignment5/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── contacts.db
│   ├── requirements.txt
│   └── README.md
└── assignment6/
    ├── app.py
    ├── kb.json
    ├── requirements.txt
    ├── templates/
    │   └── index.html
    ├── static/
    │   └── style.css
    └── README.md
```

## 🔧 Technical Requirements

### Python Packages Needed
```
# Core Python (Assignments 1-2)
- Built-in libraries only

# Data Science (Assignment 3)
pandas>=1.3.0
numpy>=1.21.0

# Machine Learning (Assignment 4)
tensorflow>=2.8.0
matplotlib>=3.5.0
pillow>=8.0.0

# Web Development (Assignment 5)
fastapi>=0.68.0
uvicorn>=0.15.0
sqlite3 (built-in)
pydantic>=1.8.0

# Chatbot (Assignment 6)
flask>=2.0.0
openai>=1.0.0
python-dotenv>=0.19.0
```

## ✅ Success Criteria Checklist

### General Requirements
- [ ] All code runs without errors
- [ ] Proper error handling implemented
- [ ] Clean, readable code with comments
- [ ] All input validation working
- [ ] Output formatting matches specifications
- [ ] Documentation included where required

### Assignment-Specific Success Metrics
- [ ] **Assignment 1**: Correctly handles 5 students, accurate calculations
- [ ] **Assignment 2**: Reads/writes files properly, function works correctly
- [ ] **Assignment 3**: Handles missing data, accurate NumPy calculations
- [ ] **Assignment 4**: Model trains and achieves >70% accuracy
- [ ] **Assignment 5**: All CRUD operations working, validation passes
- [ ] **Assignment 6**: Chat works, safety redirects active, disclaimers visible

## 🚀 Getting Started

1. **Set up project structure**:
   ```bash
   mkdir exam-solutions
   cd exam-solutions
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv exam_env
   source exam_env/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies** (as needed per assignment)

4. **Start with Assignment 1** and work systematically through the plan

## 📝 Notes
- Each assignment should be completed in its own folder
- Test each assignment thoroughly before moving to the next
- Keep track of time spent on each assignment
- Document any assumptions or limitations
- Create sample data files as needed for testing

---

**Created**: November 15, 2025  
**Status**: Ready for implementation
