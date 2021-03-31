# ADDI Data Extractor
Extracts relevant data from the IBM Application Discovery database for ingestion into Cloud Transformation Insights.
The extracts comply with the CTI meta model (and MAM ontology). In case the meta model/ontology is changed, then the `.sql` files
in the `sql` folder should be updated.

# Prerequisites
1. Python
2. The Python package called `pymssql`. Installation instructions [here](https://docs.microsoft.com/en-us/sql/connect/python/pymssql/step-1-configure-development-environment-for-pymssql-python-development?view=sql-server-ver15)

# Run
1. Set connection parameters for the AD MSSQL database and the output folder for the CSV files in `config/addi.conf`
2. Make sure the output folder exists
3. From the project base folder, run:
```
./scripts/extract_ad_data
```
