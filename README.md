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

Specific to CPPS application: to convert the application names using naming conventions used in the applications
```
./scripts/cpps_apps_split <list-of-files-to-be-processed>
```
Wild cards for the list also work. Files will be changed in place and original files would be saved with a .bak extension.

# ADDI configuration
## Security settings for each relevant project DB:
1. In the Security->logins-><username> go to UserMapping, and for the relevant project DB enable db_owner role
