#!/usr/bin/env python3
"""
Assignment 3: Data Analysis Using Pandas & NumPy
Duration: 20 minutes
Focus: NumPy, Pandas, Data Cleaning, and Basic Statistics

This program:
1. Loads students_scores.csv using Pandas
2. Replaces missing values (NaN) with the mean of that column
3. Uses NumPy to calculate overall average score for each student
4. Finds the highest and lowest average score in the class
5. Creates a new 'Average' column and saves updated data to CSV
"""

import pandas as pd
import numpy as np
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def load_student_data(filename: str) -> pd.DataFrame:
    """
    Load student data from CSV file.
    
    Args:
        filename (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded student data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.EmptyDataError: If file is empty
    """
    try:
        df = pd.read_csv(filename)
        print(f"Successfully loaded data from '{filename}'")
        print(f"Dataset shape: {df.shape}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"File '{filename}' is empty")
    except Exception as e:
        raise Exception(f"Error loading file '{filename}': {e}")

def display_data_info(df: pd.DataFrame, title: str) -> None:
    """Display information about the dataset."""
    print(f"\n{'='*50}")
    print(f"           {title}")
    print(f"{'='*50}")
    print(f"\nDataset Overview:")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nMissing values:")
    print(df.isnull().sum())

def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace missing values (NaN) with the mean of each column.
    
    Args:
        df (pd.DataFrame): DataFrame with potentially missing values
        
    Returns:
        pd.DataFrame: DataFrame with missing values filled
    """
    df_cleaned = df.copy()
    
    # Identify numeric columns (exclude Name column)
    numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
    
    print(f"\nCleaning missing values in columns: {list(numeric_columns)}")
    
    # Calculate and display means for each numeric column
    for col in numeric_columns:
        if df_cleaned[col].isnull().any():
            mean_value = df_cleaned[col].mean()
            missing_count = df_cleaned[col].isnull().sum()
            print(f"Column '{col}': {missing_count} missing values, mean = {mean_value:.2f}")
            df_cleaned[col].fillna(mean_value, inplace=True)
    
    return df_cleaned

def calculate_student_averages(df: pd.DataFrame) -> np.ndarray:
    """
    Calculate overall average score for each student using NumPy.
    
    Args:
        df (pd.DataFrame): DataFrame with student scores
        
    Returns:
        np.ndarray: Array of average scores for each student
    """
    # Get numeric columns only (exclude Name column)
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    # Extract numeric data as NumPy array
    scores_array = df[numeric_columns].values
    
    # Calculate average for each student (each row)
    averages = np.mean(scores_array, axis=1)
    
    return averages

def find_extremes(df: pd.DataFrame, averages: np.ndarray) -> tuple:
    """
    Find students with highest and lowest average scores.
    
    Args:
        df (pd.DataFrame): DataFrame with student data
        averages (np.ndarray): Array of average scores
        
    Returns:
        tuple: (highest_student, highest_score, lowest_student, lowest_score)
    """
    # Find indices of max and min averages
    max_idx = np.argmax(averages)
    min_idx = np.argmin(averages)
    
    # Get student names and scores
    highest_student = df.iloc[max_idx]['Name']
    highest_score = averages[max_idx]
    
    lowest_student = df.iloc[min_idx]['Name']
    lowest_score = averages[min_idx]
    
    return highest_student, highest_score, lowest_student, lowest_score

def add_average_column(df: pd.DataFrame, averages: np.ndarray) -> pd.DataFrame:
    """
    Add Average column to the DataFrame.
    
    Args:
        df (pd.DataFrame): Original DataFrame
        averages (np.ndarray): Calculated averages
        
    Returns:
        pd.DataFrame: DataFrame with Average column added
    """
    df_with_avg = df.copy()
    df_with_avg['Average'] = np.round(averages, 2)
    return df_with_avg

def display_statistics(df: pd.DataFrame, averages: np.ndarray) -> None:
    """Display comprehensive statistics."""
    print(f"\n{'='*60}")
    print(f"           STATISTICAL ANALYSIS")
    print(f"{'='*60}")
    
    # Basic statistics
    print(f"\nBasic Statistics:")
    print(f"Number of students: {len(averages)}")
    print(f"Overall class average: {np.mean(averages):.2f}")
    print(f"Standard deviation: {np.std(averages):.2f}")
    print(f"Median score: {np.median(averages):.2f}")
    
    # Find extremes
    highest_student, highest_score, lowest_student, lowest_score = find_extremes(df, averages)
    
    print(f"\nExtreme Values:")
    print(f"Highest Average: {highest_score:.1f} by {highest_student}")
    print(f"Lowest Average: {lowest_score:.1f} by {lowest_student}")
    
    # Subject-wise statistics
    print(f"\nSubject-wise Statistics:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        mean_score = df[col].mean()
        std_score = df[col].std()
        print(f"{col:<10}: Mean = {mean_score:5.1f}, Std = {std_score:5.1f}")

def save_updated_data(df: pd.DataFrame, filename: str) -> None:
    """
    Save the updated DataFrame to CSV file.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        filename (str): Output filename
    """
    try:
        df.to_csv(filename, index=False)
        print(f"\nUpdated data saved to '{filename}'")
    except Exception as e:
        print(f"Error saving file '{filename}': {e}")

def main():
    """Main function to perform data analysis."""
    input_file = "students_scores.csv"
    output_file = "students_scores_updated.csv"
    
    try:
        # Step 1: Load the dataset
        print("Step 1: Loading student data...")
        df = load_student_data(input_file)
        display_data_info(df, "ORIGINAL DATA")
        
        # Step 2: Clean missing values
        print(f"\nStep 2: Cleaning missing values...")
        df_cleaned = clean_missing_values(df)
        display_data_info(df_cleaned, "CLEANED DATA")
        
        # Step 3: Calculate averages using NumPy
        print(f"\nStep 3: Calculating student averages using NumPy...")
        averages = calculate_student_averages(df_cleaned)
        
        # Step 4: Add Average column
        print(f"\nStep 4: Adding Average column...")
        df_final = add_average_column(df_cleaned, averages)
        
        # Step 5: Display results
        display_statistics(df_cleaned, averages)
        
        # Display final dataset
        print(f"\n{'='*60}")
        print(f"           FINAL DATASET")
        print(f"{'='*60}")
        print(df_final.round(2))
        
        # Step 6: Save updated data
        print(f"\nStep 6: Saving updated data...")
        save_updated_data(df_final, output_file)
        
        # Verification
        print(f"\nVerification - Sample output format:")
        highest_student, highest_score, lowest_student, lowest_score = find_extremes(df_cleaned, averages)
        print(f"Highest Average: {highest_score:.1f} by {highest_student}")
        print(f"Lowest Average: {lowest_score:.1f} by {lowest_student}")
        print(f"Updated file saved as {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
