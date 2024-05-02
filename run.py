import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import math

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data form the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break
    
    return sales_data
    print(data)
    

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cnanot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required. You provided {len(values)}"
            ) 
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False

    return True


#def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    
    The surplus is defined as the sales figure subtracted from the stock.
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock.pop()
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus_data.append(int(stock) - sales)   
    
    return surplus_data


#def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided.
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully.\n")



def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet.
    Updates the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet.capitalize()} worksheet updated successfully.\n")



def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")    
    columns = []
    for x in range(6):
        x += 1
        slice = sales.col_values(x)
        columns.append(slice[-5:])

    return columns
    

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    stock_recs = []
    for column in data:
        avg = sum([int(y) for y in column])/(len(data))
        avg = math.ceil(avg)
        rec_sandwiches = math.ceil(avg * 1.1)
        stock_recs.append(rec_sandwiches)
    return stock_recs

    #sales_columns / 5 = average
    #append average to list
    #update worksheet
    #print recommendations

def print_recs():
    """
    Prints stock recommendations for the next market
    """
    print("Stock recommendations for next market...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_item_type = stock[0]
    stock_recommended_no = stock[-1]
    for item_type, num in zip(stock_item_type, stock_recommended_no):
        print(f"{item_type.capitalize()}: {num}")  



def main():
    """
    Run all programs function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_colummns = get_last_5_entries_sales()
    calculate_stock_data(sales_colummns)
    stock_rec_data = calculate_stock_data(sales_colummns)
    update_worksheet(stock_rec_data, "stock")
    print_recs()


print("Welcome to Love Sandwiches Data Automation")
main()

