# MFS Record Filter

A graphical desktop application for filtering and displaying records of Mobile Financial Services (MFS) transactions using Python’s Tkinter library.

## Overview

The MFS Record Filter application allows users to filter transaction records by various criteria such as MFS name, status, transaction status, and date range, as well as search within records for specific terms. The application reads data from a CSV file and displays filtered records in a table view.

### Key Features

- **Filter by Multiple Criteria**: Filter MFS records based on MFS name, status, transaction status, and other criteria.
- **Date Range Filtering**: Specify a start and end date to narrow down records by transaction date.
- **Paginated Results**: Use limit and offset to control the number of displayed records.
- **Search Capability**: Search within records for specific keywords across multiple fields.
- **CSV Data Source**: Load MFS transaction data from a CSV file.

## Requirements

- **Python 3.8+**
- **Tkinter** (included in standard Python library)
- **CSV file** containing MFS transaction records

### Sample CSV Format

The CSV file should have the following headers:

```text
mfs_name,status,mfs_transaction_status,created_by,debit_account_number,debit_account_title,credit_account_title,cbs_ft_trace_no,credit_account_number,debit_account_branch_oid,created_on
```

## Installation

1. Clone the repository or download the code files.
2. Ensure the required libraries are available (Tkinter is included in standard Python).
3. Place the CSV file (`sample_mfs_data.csv`) in the same directory as the script or specify its path in the code.

## Usage

1. **Run the application**: Launch the application by running the script:

    ```bash
    python recordFiltering.py
    ```

2. **Filter Records**:
   - Enter filtering criteria in the input fields:
     - `MFS Name`, `Status`, and `Transaction Status` filter specific fields.
     - `Search Term` looks for the term across multiple fields like account numbers, account titles, etc.
     - `Start Date` and `End Date` (format: YYYY-MM-DD) narrow results to a date range.
     - `Limit` and `Offset` control pagination.
   - Click the **Filter** button to apply the filters and view results in the table.

3. **View Results**: Filtered records appear in a table with columns `MFS Name`, `Status`, `Transaction Status`, `Created By`, and `Created On`.

## Code Structure

- `csv_to_dict_list(file_path)`: Reads a CSV file and converts it into a list of dictionaries.
- `fetch_mfs_records(...)`: Filters records based on provided criteria and returns paginated results.
- `MFSFilterApp`: Tkinter class that creates the graphical interface, handles user input, and displays results.

## Example

Here is a sample entry in `sample_mfs_data.csv`:

```csv
mfs_name,status,mfs_transaction_status,created_by,debit_account_number,debit_account_title,credit_account_title,cbs_ft_trace_no,credit_account_number,debit_account_branch_oid,created_on
example_mfs,active,success,user123,123456,Account A,Account B,trace123,654321,branch1,2023-05-15
```

## Troubleshooting

- **UnicodeDecodeError**: Ensure the CSV file is saved with UTF-8 encoding.
- **Missing Columns**: Verify the CSV file contains the necessary headers.
