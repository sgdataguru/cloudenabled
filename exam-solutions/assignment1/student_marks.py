#!/usr/bin/env python3
"""
Assignment 1: Python Data & Control Practice
Duration: 20 minutes
Focus: Variables, Data Types, Operators, Lists, Tuples, Dictionaries

This program:
1. Asks user to enter five student names and their marks out of 100
2. Stores data in a dictionary (name → marks)
3. Calculates and displays:
   - The average mark
   - The name(s) of the student(s) with the highest mark
   - A sorted list of all students in alphabetical order
   - All students who scored above the average
"""

def collect_student_data():
    """Collect student names and marks from user input."""
    students = {}
    print("=== Student Marks Collection System ===")
    print("Please enter details for 5 students:\n")
    
    for i in range(1, 6):
        while True:
            try:
                # Get student name
                name = input(f"Enter student {i} name: ").strip()
                if not name:
                    print("Name cannot be empty. Please try again.")
                    continue
                
                # Get marks with validation
                marks = float(input(f"Enter marks for {name} (out of 100): "))
                
                if marks < 0 or marks > 100:
                    print("Marks must be between 0 and 100. Please try again.")
                    continue
                
                students[name] = marks
                break
                
            except ValueError:
                print("Please enter a valid number for marks.")
            except KeyboardInterrupt:
                print("\nProgram interrupted by user.")
                return None
    
    return students

def calculate_average(students):
    """Calculate the average marks of all students."""
    if not students:
        return 0
    return sum(students.values()) / len(students)

def find_top_scorers(students):
    """Find the student(s) with the highest marks."""
    if not students:
        return []
    
    max_marks = max(students.values())
    top_scorers = [name for name, marks in students.items() if marks == max_marks]
    return top_scorers, max_marks

def get_sorted_students(students):
    """Get students sorted alphabetically by name."""
    return sorted(students.keys())

def find_above_average_students(students, average):
    """Find students who scored above the average."""
    return [name for name, marks in students.items() if marks > average]

def display_results(students):
    """Display all calculated results in a formatted manner."""
    if not students:
        print("No student data to display.")
        return
    
    print("\n" + "="*50)
    print("           STUDENT MARKS ANALYSIS")
    print("="*50)
    
    # Calculate average
    average = calculate_average(students)
    print(f"\nAverage marks: {average:.1f}")
    
    # Find top scorers
    top_scorers, max_marks = find_top_scorers(students)
    if len(top_scorers) == 1:
        print(f"Top scorer: {top_scorers[0]} with {max_marks} marks")
    else:
        print(f"Top scorers: {', '.join(top_scorers)} with {max_marks} marks each")
    
    # Display sorted list
    sorted_students = get_sorted_students(students)
    print(f"\nStudents in alphabetical order: {sorted_students}")
    
    # Find above average students
    above_average = find_above_average_students(students, average)
    if above_average:
        print(f"Students above average: {above_average}")
    else:
        print("No students scored above average.")
    
    # Display detailed breakdown
    print(f"\nDetailed Results:")
    print("-" * 30)
    for name in sorted_students:
        marks = students[name]
        status = "Above Average" if marks > average else "Below Average" if marks < average else "Average"
        print(f"{name:<15}: {marks:>6.1f} ({status})")

def main():
    """Main function to run the student marks analysis program."""
    try:
        # Collect student data
        students = collect_student_data()
        
        if students is None:
            return
        
        if not students:
            print("No student data collected.")
            return
        
        # Display results
        display_results(students)
        
        # Save results to file for verification
        with open('student_results.txt', 'w') as f:
            f.write("Student Marks Analysis Results\n")
            f.write("="*40 + "\n\n")
            
            average = calculate_average(students)
            f.write(f"Average marks: {average:.1f}\n")
            
            top_scorers, max_marks = find_top_scorers(students)
            if len(top_scorers) == 1:
                f.write(f"Top scorer: {top_scorers[0]} with {max_marks} marks\n")
            else:
                f.write(f"Top scorers: {', '.join(top_scorers)} with {max_marks} marks each\n")
            
            sorted_students = get_sorted_students(students)
            f.write(f"Students in alphabetical order: {sorted_students}\n")
            
            above_average = find_above_average_students(students, average)
            f.write(f"Students above average: {above_average}\n")
        
        print(f"\nResults also saved to 'student_results.txt'")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
