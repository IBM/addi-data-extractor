"""
Licensed Materials - Property of IBM

(C) Copyright IBM Corp. 1996,2018

US Government Users Restricted Rights - Use, duplication or
disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
"""

# List ADDI database(s) to import into the Modernization Fabric
addi_repository_list = (["xx.xx.xx.xx,DatabaseName,DatabaseAlias,username,password"])

# Specify .csv file output directory
csv_output_directory = ""

## To run all sql files in the sql folder assign this to an empty list
addi_sql_list=[]

## PLEASE DONT EDIT THE PRE-PROCESS AND POST-PROCESS LIST
preprocess_sql_list=['GetVarPreoutput.sql',
                    'GetFinalProgName.sql',
                    'GetCobolLocal.sql',
                    'GetCobolCopy.sql',
                    'GetPL1Local.sql',
                    'GetPL1Copy.sql']
postprocess_sql_list=[]

## To run only selected sql files, uncomment this line and put them in the list.
# addi_sql_list=[]
