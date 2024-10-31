# Datasets_to_sqlite
This project includes Python scripts to convert a collection of datasets into an SQLite database, enabling easy data management and analysis.

## Requirements
- Python 3.7 or higher
- SQLite
- Pandas

## Installation

To run the project locally, follow these steps:

1. **Clone this repository:**
   ```bash
   git clone https://github.com/JDMatu/Datasets_to_sqlite.git

2. **Navigate to the project directory:**
   ```bash
   $ cd Datasets_to_sqlite

> [!TIP]
> **Create a virtual environment:** This helps avoid installing dependencies globally on your system.
   ```bash
   $ python3 -m venv venv
   $ source venv/bin/activate  # For Linux or macOS
   # Or for Windows
   # venv\Scripts\activate
   ```

3. **Install the necessary dependencies:** If you created a virtual environment, install the required dependencies using the following command:

   ```bash
    $ pip install -r requirements.txt
    # or
    # $ pip install pandas

4. **Download a dataset:** The project includes a folder named 'F1_Datasets' containing several CSV files related to Formula 1. You can replace this with your folder containing your datasets.

- You can download datasets from [Kaggle](https://www.kaggle.com/) or your preferred source.

5. **Create the database:** Run the script 'crear_db.py' in the terminal using the following command:

    ```bash
    $ python crear_db.py

6. **Establish relationships:** If you need primary keys and foreign keys in your database, you'll need to modify the `add_relaciones.py` file.

   - **Modify the `table_definitions` list:** If you are using a different dataset than the one provided, you should change the table definitions based on the DataFrames in your CSV files.
    
   - **Execute the file:** Once you have updated the file with the correct definitions, you can run the script in the terminal with the following command:
   
   ```bash
   $ python add_relaciones.py