import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(file_path):
    try:
        excel_file = pd.ExcelFile(file_path, engine='openpyxl')
        print("Available Sheet Names:", excel_file.sheet_names)

        # Read specific sheets
        user_details = pd.read_excel(file_path, sheet_name='UserDetails.csv', engine='openpyxl')
        cooking_sessions = pd.read_excel(file_path, sheet_name='CookingSessions.csv', engine='openpyxl')
        order_details = pd.read_excel(file_path, sheet_name='OrderDetails.csv', engine='openpyxl')
        
        return user_details, cooking_sessions, order_details
    except Exception as e:
        print("An error occurred while loading data:", e)
        raise


def clean_data(user_details, cooking_sessions, order_details):
    user_details["Registration Date"] = pd.to_datetime(user_details["Registration Date"])
    order_details["Order Date"] = pd.to_datetime(order_details["Order Date"])
    cooking_sessions["Session Start"] = pd.to_datetime(cooking_sessions["Session Start"])
    cooking_sessions["Session End"] = pd.to_datetime(cooking_sessions["Session End"])
    

    user_details.fillna({"Favorite Meal": "Unknown"}, inplace=True)
    order_details.dropna(inplace=True)
    

    cooking_sessions["Meal Type"] = cooking_sessions["Meal Type"].str.lower()
    order_details["Meal Type"] = order_details["Meal Type"].str.lower()
    
    return user_details, cooking_sessions, order_details


def merge_data(user_details, cooking_sessions, order_details):
    user_sessions = pd.merge(cooking_sessions, user_details, on="User ID", how="left")
    full_data = pd.merge(user_sessions, order_details, on=["User ID", "Session ID"], how="left")
    return full_data


def analyze_data(full_data):
    try:
        print("Columns in full_data:", full_data.columns)

        # Handle potential column mismatch
        if "Dish Name_x" in full_data.columns or "Dish Name_y" in full_data.columns:
            full_data["Dish Name"] = full_data["Dish Name_x"].combine_first(full_data["Dish Name_y"])

        # Check for 'Dish Name' column
        if "Dish Name" in full_data.columns:
            popular_dishes = full_data["Dish Name"].value_counts().head(10)
        else:
            print("Column 'Dish Name' not found.")
            popular_dishes = pd.Series(dtype="int")  # Empty Series as fallback

        # Aggregate sessions and orders
        sessions_to_orders = full_data.groupby("Session ID").agg({"Order ID": "nunique"})
        sessions_to_orders.reset_index(inplace=True)
        sessions_to_orders.rename(columns={"Order ID": "Orders"}, inplace=True)
        
        return popular_dishes, sessions_to_orders
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        raise

def visualize_data(popular_dishes, sessions_to_orders):
    # Bar plot for popular dishes
    popular_dishes.plot(kind='bar', title='Top 10 Popular Dishes', figsize=(10, 6))
    plt.xlabel('Dish Name')
    plt.ylabel('Count')
    plt.show()
    
    # Scatter plot for orders
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="Session ID", y="Orders", data=sessions_to_orders)
    plt.title("Sessions vs Orders for Dishes")
    plt.show()

        



def visualize_data(popular_dishes, sessions_to_orders):
    # Bar plot for popular dishes
    popular_dishes.plot(kind='bar', title='Top 10 Popular Dishes', figsize=(10, 6))
    plt.xlabel('Dish Name')
    plt.ylabel('Count')
    plt.show()
    
    # Scatter plot for orders
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="Sessions", y="Orders", data=sessions_to_orders)
    plt.title("Sessions vs Orders for Dishes")
    plt.show()


if __name__ == "__main__":
  
    file_path = "/Users/shivanshidheer/upliance-data-analysis/data/Excel.xlsx"
    
   
    user_details, cooking_sessions, order_details = load_data(file_path)
    
    # Clean data
    user_details, cooking_sessions, order_details = clean_data(user_details, cooking_sessions, order_details)
    
    # Merge data
    full_data = merge_data(user_details, cooking_sessions, order_details)
    

    popular_dishes, sessions_to_orders = analyze_data(full_data)
    
 
    visualize_data(popular_dishes, sessions_to_orders)
