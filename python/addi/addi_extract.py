import csv
import pymssql
import pandas as pd

from addiconf import addi_repository_list, csv_output_directory
from settings import sql_file_directory, addi_sql_list

# Iterate through addi-sql-list
i = 0
sqllistsize = len(addi_sql_list)
while i < sqllistsize:

    # iterate through addi repositories and run addi SQL against each repository
    j = 0
    addilistsize = len(addi_repository_list)
    setcolumnnames = 'N'
    print("i --- " + addi_sql_list[i])
    while j < addilistsize:

        addi_repository_list_split = addi_repository_list[j].split(",")
        if len(addi_repository_list_split ) != 5:
            print("addi_repository_list entry does not have host, addidb, dbpfx, username, password: ", addi_repository_list[j])
        else:
            # set host, addidb, dbpfx, username, and password for creating connection to MS SQL Server
            host = addi_repository_list_split[0]
            # print("host: ", host)

            addidb = addi_repository_list_split[1]
            # print("addidb: ", addidb)

            dbpfx = addi_repository_list_split[2]
            # print("dbpfx: ", dbpfx)

            username = addi_repository_list_split[3]
            # print ("username: ", username)

            password = addi_repository_list_split[4]
            # print("password: ", password)

            # Establish connection to MS SQL Server
            cnxn = pymssql.connect(host, username, password, addidb)
            cursor = cnxn.cursor()

            # retrieve SQL statement from sql file folder
            f = open(sql_file_directory + '/' + addi_sql_list[i], 'r', encoding="utf8", errors='ignore')
            dataString = f.read().strip()
            f.close()

            # replace sql statement with database name and key field prefix to differentiate
            # multiple addi respositories and make sure unique keys are maintained for objects
            # across addi repositories
            dataString = dataString.replace("<addidb>", addidb)
            dataString = dataString.replace("<dbpfx>", dbpfx)
            # print(dataString)

            # Execute sql stateemnt
            cursor.execute(dataString)

            # Put SQL results into dataframe and accumulate sql results across addi respositories
            df1 = pd.DataFrame(cursor.fetchall())
            if cursor.rowcount == 0:
                print('sql query returned no data', addi_sql_list[i], " - ", addidb)
            else:
                if setcolumnnames == 'N':
                    column_names = [item[0] for item in cursor.description]
                    df1.columns = column_names
                    setcolumnnames = 'Y'
                    df2 = df1
                else:
                    column_names = [item[0] for item in cursor.description]
                    df1.columns = column_names
                    df2 = pd.concat([df2,df1])
        j += 1

    # Close MS SQL connection
    cnxn.close()
    if setcolumnnames == 'N':
        print("no data found on any database when running: ", addi_sql_list[i])
    else:
        # Output the dataframe to a .csv file
        outputFileName = addi_sql_list[i].replace(".sql", ".csv")
        df2.to_csv(csv_output_directory + '/' + outputFileName, encoding='utf-8', index=False)
    i += 1

# Check to see if settings.py had any problems (i.e. no data provided)
if sqllistsize == 0:
    print("no sql files specified in settings.py file")
if addilistsize == 0:
    print ("no addi respositories specified in settings.py")

