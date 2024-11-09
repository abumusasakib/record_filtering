import tkinter as tk
from tkinter import ttk
from datetime import datetime

import csv

def csv_to_dict_list(file_path):
    # Initialize an empty list to store each row as a dictionary
    records = []
    
    # Open the CSV file with utf-8 encoding
    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        # Create a DictReader to read each row as a dictionary
        csv_reader = csv.DictReader(csv_file)
        
        # Iterate over each row in the CSV and add it to the list
        for row in csv_reader:
            # Append each row dictionary to the records list
            records.append(row)
    
    return records

# Usage
file_path = 'sample_mfs_data.csv'  # Replace with the path to your CSV file
sample_records = csv_to_dict_list(file_path)

# # Print the list of dictionaries
# for record in sample_records:
#     print(record)


# # Sample records to simulate the data source
# sample_records = [
#     {
#         "mfs_name": "example_mfs",
#         "status": "active",
#         "mfs_transaction_status": "success",
#         "created_by": "user123",
#         "debit_account_number": "123456",
#         "debit_account_title": "Account A",
#         "credit_account_title": "Account B",
#         "cbs_ft_trace_no": "trace123",
#         "credit_account_number": "654321",
#         "debit_account_branch_oid": "branch1",
#         "created_on": "2023-05-15"
#     },
#     # Add more sample records as needed
# ]

def fetch_mfs_records(
    records,
    mfs_name=None,
    status=None,
    mfs_transaction_status=None,
    search_term=None,
    start_date=None,
    end_date=None,
    limit=10,
    offset=0
):
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    filtered_records = []
    for record in records:
        if mfs_name and record.get("mfs_name") != mfs_name:
            continue
        if status and record.get("status") != status:
            continue
        if mfs_transaction_status and record.get("mfs_transaction_status") != mfs_transaction_status:
            continue
        if search_term:
            search_pattern = search_term.lower()
            if not (
                search_pattern in str(record.get("created_by", "")).lower() or
                search_pattern in str(record.get("debit_account_number", "")).lower() or
                search_pattern in str(record.get("debit_account_title", "")).lower() or
                search_pattern in str(record.get("credit_account_title", "")).lower() or
                search_pattern in str(record.get("cbs_ft_trace_no", "")).lower() or
                search_pattern in str(record.get("credit_account_number", "")).lower() or
                search_pattern in str(record.get("debit_account_branch_oid", "")).lower()
            ):
                continue
        created_on = datetime.strptime(record.get("created_on"), "%Y-%m-%d")
        if start_date and created_on < start_date:
            continue
        if end_date and created_on > end_date:
            continue
        
        filtered_records.append(record)
    
    filtered_records.sort(key=lambda x: x.get("created_on"), reverse=True)
    return filtered_records[offset:offset + limit]

class MFSFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MFS Record Filter")
        
        # Define input fields
        self.mfs_name_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.mfs_transaction_status_var = tk.StringVar()
        self.search_term_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.limit_var = tk.IntVar(value=10)
        self.offset_var = tk.IntVar(value=0)
        
        # Create input form
        self.create_input_form()
        
        # Table to display results
        self.create_result_table()
        
    def create_input_form(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Labels and Entries
        tk.Label(frame, text="MFS Name").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.mfs_name_var).grid(row=0, column=1, sticky="ew")
        
        tk.Label(frame, text="Status").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.status_var).grid(row=1, column=1, sticky="ew")
        
        tk.Label(frame, text="Transaction Status").grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.mfs_transaction_status_var).grid(row=2, column=1, sticky="ew")
        
        tk.Label(frame, text="Search Term").grid(row=3, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.search_term_var).grid(row=3, column=1, sticky="ew")
        
        tk.Label(frame, text="Start Date (YYYY-MM-DD)").grid(row=4, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.start_date_var).grid(row=4, column=1, sticky="ew")
        
        tk.Label(frame, text="End Date (YYYY-MM-DD)").grid(row=5, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.end_date_var).grid(row=5, column=1, sticky="ew")
        
        tk.Label(frame, text="Limit").grid(row=6, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.limit_var).grid(row=6, column=1, sticky="ew")
        
        tk.Label(frame, text="Offset").grid(row=7, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.offset_var).grid(row=7, column=1, sticky="ew")
        
        # Submit button
        tk.Button(frame, text="Filter", command=self.filter_records).grid(row=8, column=0, columnspan=2, pady=10)
    
    def create_result_table(self):
        self.tree = ttk.Treeview(self.root, columns=("mfs_name", "status", "transaction_status", "created_by", "created_on"), show="headings")
        self.tree.heading("mfs_name", text="MFS Name")
        self.tree.heading("status", text="Status")
        self.tree.heading("transaction_status", text="Transaction Status")
        self.tree.heading("created_by", text="Created By")
        self.tree.heading("created_on", text="Created On")
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def filter_records(self):
        # Get filter values from input fields
        mfs_name = self.mfs_name_var.get()
        status = self.status_var.get()
        mfs_transaction_status = self.mfs_transaction_status_var.get()
        search_term = self.search_term_var.get()
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        limit = self.limit_var.get()
        offset = self.offset_var.get()
        
        # Fetch filtered records
        records = fetch_mfs_records(
            sample_records, 
            mfs_name=mfs_name, 
            status=status, 
            mfs_transaction_status=mfs_transaction_status,
            search_term=search_term, 
            start_date=start_date, 
            end_date=end_date,
            limit=limit, 
            offset=offset
        )
        
        # Clear previous results
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Insert new results into the table
        for record in records:
            self.tree.insert("", "end", values=(
                record["mfs_name"],
                record["status"],
                record["mfs_transaction_status"],
                record["created_by"],
                record["created_on"]
            ))

# Create the Tkinter app
root = tk.Tk()
app = MFSFilterApp(root)
root.mainloop()
