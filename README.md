# workshop1-ETL
**Made by**: Estefanía Hernández Rojas
## ETL pipeline
The goal of this project is to build ETL pipeline: extract from a CSV, transform it intro a Dimensional Data Model, load it into a Data Warehouse and generate reports with KPIs and visualizations directly from the DW. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/473a1f3d-d711-4867-a94a-62b52943d663" alt="workshop 1 Diagram" width="751">
</p>

1. **Extract**  
   - Source: Raw CSV file with application data.  
2. **Transform**  
   - Data cleaning and normalization using **Python & Pandas**.  
   - Creation of surrogate keys for each dimension.  
   - Splitting the dataset into **dimension tables** and the **fact table**.  
3. **Load**  
   - Loading into MySQL Data Warehouse.  
   - Dimensions are inserted first, followed by the fact table with foreign keys.  

## Star Schema
The design follows a **Star Schema**:
- **Fact Table:** `fact_application` (contains candidate applications, scores, hire flag)
- **Dimension Tables:**  
  - `dim_candidate` (first name, last name, email)  
  - `dim_country` (country)  
  - `dim_technology` (technology)  
  - `dim_seniority` (seniority)  
  - `dim_date` (application date, year, month, day)

<p align="center">
  <img src="https://github.com/HEstefaniaR/workshop1-ETL/blob/main/diagrams/Star%20Schema.png" alt="Star Schema" width="751">
</p>

This design allows for efficient joins between fact and dimensions, enabling detailed analysis across multiple perspectives: time, geography, technology, and seniority.

## Project Structure
```
.
├── data
│   └── candidates.csv
├── diagrams
│   └── Star Schema.png
├── etl
│   ├── connection.py
│   ├── extract.py
│   ├── load.py
│   ├── main.py
│   └── transform.py
├── report
│   ├── kpis.py
│   ├── outputs
│   │   ├── Hire rate by Technology.png
│   │   ├── Hire Rate.png
│   │   ├── Hires by Country and Year.png
│   │   ├── Hires by Seniority.png
│   │   ├── Hires by Technology.png
│   │   └── Hires by Year.png
│   └── visualization.py
├── README.md
└── requirments.txt
```
- **`data/`**: Contains the raw CSV dataset used as the source for the ETL pipeline.  
- **`diagrams/`**: Holds the Star Schema diagram and other supporting documentation.  
- **`etl/`**: Implements the ETL process.  
  - `connection.py`: manages the database connection to the Data Warehouse.  
  - `extract.py`: loads raw data from the CSV file.  
  - `transform.py`: applies business rules (e.g., "HIRED" logic) and prepares dimension/fact tables.  
  - `load.py`: inserts the transformed data into the DW.  
  - `main.py`: orchestrates the ETL pipeline (extract → transform → load).  
- **`report/`**: Contains scripts for generating KPIs and visualizations.  
  - `kpis.py`: defines SQL queries to extract metrics from the DW.  
  - `visualization.py`: creates plots (e.g., hires by technology, seniority, country).  
  - `outputs/`: stores generated visualization images.
 
## Key Decisions
### KPIs
The following KPIs were selected as the main business questions to be answered:  

- **Hires by Technology**  
  Understand which technologies are most in demand.  

- **Hires by Year**  
  Analyze how hiring evolves over time.  

- **Hires by Seniority**  
  Evaluate the focus of hiring efforts (junior vs senior roles).  

- **Hires by Country Over Time** (focused on USA, Brazil, Colombia, Ecuador)  
  Compare hiring trends across regions.  

- **Hiring Rate**  
  Percentage of candidates hired vs total applicants.  

- **Applicants vs Hires by Technology**  
  Compare supply of applicants against actual hiring demand per technology.  

## Visualizations
The queries were implemented in **MySQL** and visualized using **Python (matplotlib)**.  
These visualizations present clear insights into hiring trends across technology, seniority, geography, and time.  

## How to run the project
1. **Clone the repository**  
   ```bash
   git clone https://github.com/HEstefaniaR/workshop1-ETL
   cd workshop1-ETL
   ```

2.	Install dependencies: It is recommended to use a virtual environment.

    ```bash
    python -m venv venv
    source venv/bin/activate # Mac/Linux  
    venv\Scripts\activate    # Windows  
    
    pip install -r requirements.txt
    ```
3. Configure database connection. Open `etl/connection.py` and update the MySQL connection parameters if needed:
    ```bash
    conn = mysql.connector.connect(
            host='localhost', 
            user='your_user', 
            password='your_password',
        )
    ```
4.	Run the ETL pipeline. From the project root:
    ```bash
    python etl/main.py
    ```
5. Generate reports and visualizations. After the ETL has populated the Data Warehouse:
    ```bash
    python report/visualization.py
    ```
