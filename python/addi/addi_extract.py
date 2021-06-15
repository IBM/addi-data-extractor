import csv
import pymssql
import pandas as pd
from time import time
from addiconf import addi_repository_list, csv_output_directory
from settings import addi_sql_list, preprocess_sql_list, postprocess_sql_list
from settings import preprocess_directory, sql_file_directory, postprocess_directory

def run_sqls(sql_list,repo_list,csv_dir,sql_directory,mode) :

    # number of queries
    sqllistsize = len(sql_list)
    # number of repos
    addilistsize = len(repo_list)

    # Check to see if settings.py had any problems (i.e. no data provided)
    if sqllistsize == 0:
        print("no sql files specified in settings.py file")
        return
    if addilistsize == 0:
        print ("no addi respositories specified in settings.py")
        return

    # Iterate through addi-sql-list
    i = 0
    
    while i < sqllistsize:
        # iterate through addi repositories and run addi SQL against each repository
        j = 0
        setcolumnnames = 'N'
        print("i --- " + sql_list[i])
        while j < addilistsize:

            repo_list_split = repo_list[j].split(",")
            if len(repo_list_split ) != 5:
                print("repo_list entry does not have host, addidb, dbpfx, username, password: ", repo_list[j])
            else:
                # set host, addidb, dbpfx, username, and password for creating connection to MS SQL Server
                host = repo_list_split[0]
                # print("host: ", host)

                addidb = repo_list_split[1]
                # print("addidb: ", addidb)

                dbpfx = repo_list_split[2]
                # print("dbpfx: ", dbpfx)

                username = repo_list_split[3]
                # print ("username: ", username)

                password = repo_list_split[4]
                # print("password: ", password)

                # retrieve SQL statement from sql file folder
                f = open(sql_directory + '/' + sql_list[i], 'r', encoding="utf8", errors='ignore')
                dataString = f.read().strip()
                f.close()

                # replace sql statement with database name and key field prefix to differentiate
                # multiple addi respositories and make sure unique keys are maintained for objects
                # across addi repositories
                dataString = dataString.replace("<addidb>", addidb)
                dataString = dataString.replace("<dbpfx>", dbpfx)               

                if mode == "preprocess" :
                    try :
                        with pymssql.connect(host, username, password, addidb) as conn:
                            with conn.cursor(as_dict=True) as cursor:
                                # store the procedure
                                cursor.execute(dataString)
                                # execute the procedure
                                cursor.callproc(sql_list[i].split('.')[0])
                            # persist changes in DB
                            conn.commit()
                        print("Preprocessing Script " + sql_list[i] + " : Completed Successfully!\n")
                    except Exception as e :
                        print(e)

                elif mode == "postprocess" :
                    try :
                        with pymssql.connect(host, username, password, addidb) as conn:
                            with conn.cursor(as_dict=True) as cursor:
                                cursor.execute(dataString)
                            # persist changes in DB
                            conn.commit()
                        print("Postprocessing Script " + sql_list[i] + " : Completed Successfully!\n")
                    except Exception as e :
                        print(e)
                
                elif mode == "fetchData" :
                    try :
                        # Establish connection to MS SQL Server
                        cnxn = pymssql.connect(host, username, password, addidb)
                        cursor = cnxn.cursor()
                        # Execute sql statement
                        cursor.execute(dataString)
                        # Put SQL results into dataframe and accumulate sql results across addi respositories
                        df1 = pd.DataFrame(cursor.fetchall())
                        if cursor.rowcount == 0:
                            print('sql query returned no data', sql_list[i], " - ", addidb)
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
                        # Close MS SQL connection
                        cnxn.close()
                    except Exception as e :
                        print(e)
            j += 1

        if mode == "fetchData" and setcolumnnames == 'N':
            print("no data found on any database when running: ", sql_list[i])
        elif mode == "fetchData" and setcolumnnames == 'Y':
            # Output the dataframe to a .csv file
            outputFileName = sql_list[i].replace(".sql", ".csv")
            df2.to_csv(csv_dir + '/' + outputFileName, encoding='utf-8', index=False)
        i += 1


if __name__ == '__main__' :

    # Preprocessing Queries
    print("========================> Preprocessing Scripts <========================")
    begin = time()
    run_sqls(preprocess_sql_list,addi_repository_list,csv_output_directory,preprocess_directory,"preprocess")
    end = time()
    print("Preprocessing Time : " + str(end-begin))

    # SQL Queries for ADDI
    print("\n\n========================> Querying ADDI <========================")
    begin = time()
    run_sqls(addi_sql_list,addi_repository_list,csv_output_directory,sql_file_directory,"fetchData")
    end = time()
    print("Querying Time : " + str(end-begin))

    # Postprocessing Queries
    print("\n\n========================> Postprocessing Scripts <========================")
    begin = time()
    run_sqls(postprocess_sql_list,addi_repository_list,csv_output_directory,postprocess_directory,"postprocess")
    end = time()
    print("Postprocessing Time : " + str(end-begin))