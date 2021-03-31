"""
Licensed Materials - Property of IBM

(C) Copyright IBM Corp. 1996,2018

US Government Users Restricted Rights - Use, duplication or
disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
"""

import os
from addiconf import addi_sql_list

# Specify directory to find .sql file(s)
sql_file_directory = os.path.dirname(os.path.realpath(__file__))+"/../../sql"
print("Using SQLs in: " + sql_file_directory)

# If a list of sql files is not already provided by the user, then pick all of them
use_all = False
try:
    if (len(addi_sql_list) == 0):
        use_all = True
except NameError:
    use_all = True

if (use_all):
   addi_sql_list = []
   for file in os.listdir(sql_file_directory):
       if file.endswith(".sql"):
           print(file)
           addi_sql_list.append(file)

