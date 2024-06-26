#!/bin/env python
def increment_number_in_file(file_path):
    try:
        # Read the number from the file
        with open(file_path, 'r') as file:
            number = float(file.readline().strip())
        
        # Increment the number by 1/10
        number += 0.01
        number = int((number*100)+1)/100
        
        
        # Round the number to two decimal places
        # Write the new number back to the file
        with open(file_path, 'w') as file:
            file.write(str(number))
        
        print(number)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

# Example usage
file_path = "./.version"
increment_number_in_file(file_path)
