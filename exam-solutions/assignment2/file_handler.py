#!/usr/bin/env python3
"""
Assignment 2: File Handling & Functions
Duration: 20 minutes
Focus: File Handling, Functions, Data Processing

This program:
1. Reads data from "sales.txt" file (product_name, quantity_sold, price_per_unit)
2. Defines a function calculate_total(quantity, price) to compute total sales
3. Writes results to "sales_summary.txt" showing:
   - Product name
   - Quantity sold
   - Total sales amount
"""

import os
from typing import List, Tuple, Dict

def calculate_total(quantity: int, price: float) -> float:
    """
    Calculate total sales for a product.
    
    Args:
        quantity (int): Number of units sold
        price (float): Price per unit
        
    Returns:
        float: Total sales amount
    """
    return quantity * price

def read_sales_data(filename: str) -> List[Tuple[str, int, float]]:
    """
    Read sales data from a CSV file.
    
    Args:
        filename (str): Path to the sales data file
        
    Returns:
        List of tuples containing (product_name, quantity, price)
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If data format is invalid
    """
    sales_data = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            line_number = 0
            for line in file:
                line_number += 1
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Split by comma
                parts = line.split(',')
                
                if len(parts) != 3:
                    raise ValueError(f"Line {line_number}: Expected 3 values, got {len(parts)}")
                
                try:
                    product_name = parts[0].strip()
                    quantity = int(parts[1].strip())
                    price = float(parts[2].strip())
                    
                    # Validate values
                    if not product_name:
                        raise ValueError(f"Line {line_number}: Product name cannot be empty")
                    
                    if quantity < 0:
                        raise ValueError(f"Line {line_number}: Quantity cannot be negative")
                    
                    if price < 0:
                        raise ValueError(f"Line {line_number}: Price cannot be negative")
                    
                    sales_data.append((product_name, quantity, price))
                    
                except (ValueError, IndexError) as e:
                    raise ValueError(f"Line {line_number}: Invalid data format - {e}")
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Sales data file '{filename}' not found")
    
    return sales_data

def process_sales_data(sales_data: List[Tuple[str, int, float]]) -> List[Dict[str, any]]:
    """
    Process sales data and calculate totals.
    
    Args:
        sales_data: List of tuples containing (product_name, quantity, price)
        
    Returns:
        List of dictionaries with processed sales information
    """
    processed_data = []
    
    for product_name, quantity, price in sales_data:
        total_sales = calculate_total(quantity, price)
        
        processed_data.append({
            'product': product_name,
            'quantity': quantity,
            'price_per_unit': price,
            'total_sales': total_sales
        })
    
    return processed_data

def write_sales_summary(processed_data: List[Dict[str, any]], filename: str) -> None:
    """
    Write sales summary to a file.
    
    Args:
        processed_data: List of processed sales data
        filename: Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Sales Summary Report\n")
            file.write("=" * 40 + "\n\n")
            
            total_revenue = 0
            
            for item in processed_data:
                # Format output as specified: Product → Rs. Amount
                file.write(f"{item['product']} → Rs. {item['total_sales']:.0f}\n")
                total_revenue += item['total_sales']
            
            file.write("\n" + "-" * 40 + "\n")
            file.write(f"Total Revenue: Rs. {total_revenue:.0f}\n")
            
            # Additional detailed breakdown
            file.write("\nDetailed Breakdown:\n")
            file.write("-" * 40 + "\n")
            for item in processed_data:
                file.write(f"{item['product']:<12} | "
                          f"Qty: {item['quantity']:<3} | "
                          f"Price: Rs.{item['price_per_unit']:<5.0f} | "
                          f"Total: Rs.{item['total_sales']:<6.0f}\n")
                          
    except IOError as e:
        raise IOError(f"Error writing to file '{filename}': {e}")

def display_summary(processed_data: List[Dict[str, any]]) -> None:
    """
    Display sales summary to console.
    
    Args:
        processed_data: List of processed sales data
    """
    print("\n" + "=" * 50)
    print("           SALES SUMMARY REPORT")
    print("=" * 50)
    
    total_revenue = 0
    
    for item in processed_data:
        print(f"{item['product']} → Rs. {item['total_sales']:.0f}")
        total_revenue += item['total_sales']
    
    print("\n" + "-" * 50)
    print(f"Total Revenue: Rs. {total_revenue:.0f}")
    
    print(f"\nDetailed Breakdown:")
    print("-" * 50)
    print(f"{'Product':<12} | {'Quantity':<8} | {'Price':<8} | {'Total':<8}")
    print("-" * 50)
    
    for item in processed_data:
        print(f"{item['product']:<12} | "
              f"{item['quantity']:<8} | "
              f"Rs.{item['price_per_unit']:<5.0f} | "
              f"Rs.{item['total_sales']:<6.0f}")

def main():
    """Main function to process sales data."""
    input_file = "sales.txt"
    output_file = "sales_summary.txt"
    
    try:
        print("Reading sales data from", input_file)
        
        # Read sales data
        sales_data = read_sales_data(input_file)
        
        if not sales_data:
            print("No sales data found in the file.")
            return
        
        print(f"Found {len(sales_data)} products in sales data")
        
        # Process the data
        processed_data = process_sales_data(sales_data)
        
        # Display summary to console
        display_summary(processed_data)
        
        # Write summary to file
        write_sales_summary(processed_data, output_file)
        
        print(f"\nSales summary has been written to '{output_file}'")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the sales.txt file exists in the current directory.")
    
    except ValueError as e:
        print(f"Data Error: {e}")
        print("Please check the format of your sales data.")
    
    except IOError as e:
        print(f"File Error: {e}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
