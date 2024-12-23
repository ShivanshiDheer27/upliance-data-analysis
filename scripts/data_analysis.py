import os
import pandas as pd

# Debugging: Print current working directory
print("Current Working Directory:", os.getcwd())

# File path
file_path = "data/Excel.xlsx"

# Step 1: Load Data
def load_data(file_path):
    # Debugging: Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    user_details = pd.read_excel(file_path, sheet_name='UserDetails')
    cooking_sessions = pd.read_excel(file_path, sheet_name='CookingSessions')
    order_details = pd.read_excel(file_path, sheet_name='OrderDetails')
    return user_details, cooking_sessions, order_details

# Main function
if __name__ == "__main__":
    try:
        # Load data
        user_details, cooking_sessions, order_details = load_data(file_path)
        print("Data loaded successfully!")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as e:
        print("An error occurred:", e)
