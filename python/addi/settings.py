"""
Licensed Materials - Property of IBM

(C) Copyright IBM Corp. 1996,2018

US Government Users Restricted Rights - Use, duplication or
disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
"""

import os
from addiconf import addi_sql_list,preprocess_sql_list,postprocess_sql_list

# Specify directory to find .sql file(s)
sql_file_directory = os.path.dirname(os.path.realpath(__file__))+"/../../sql"
print("Using SQLs in: " + sql_file_directory)

preprocess_directory = os.path.dirname(os.path.realpath(__file__))+"/../../sql/preprocess"
print("Using Preprocess SQLs in: " + preprocess_directory)

postprocess_directory = os.path.dirname(os.path.realpath(__file__))+"/../../sql/postprocess"
print("Using Postprocess SQLs in: " + postprocess_directory)

# If a list of sql files is not already provided by the user, then pick all of them
preprocess_all = False
postprocess_all = False
use_all = False
try:
    if (len(addi_sql_list) == 0):
        use_all = True
    
    if (len(preprocess_sql_list)==0):
        preprocess_all = True

    if (len(postprocess_sql_list)==0):
        postprocess_all = True

except NameError:
    use_all = True
    preprocess_all = True
    postprocess_all = True

if (preprocess_all) :
    # Preprocessing Scripts
    print("==> Preprocessing Scripts <==")
    preprocess_sql_list = []
    for file in os.listdir(preprocess_directory):
       if file.endswith(".sql"):
           print(file)
           preprocess_sql_list.append(file)
    print()

if (use_all):
    print("==> Normal SQL Scripts <==")
    # Normal ADDI scripts
    addi_sql_list = []
    for file in os.listdir(sql_file_directory):
        if file.endswith(".sql"):
            print(file)
            addi_sql_list.append(file)
    print()

if (postprocess_all) :
    print("==> Postprocessing Scripts <==")
    # Postprocessing Scripts
    postprocess_sql_list = []
    for file in os.listdir(postprocess_directory):
        if file.endswith(".sql"):
            print(file)
            postprocess_sql_list.append(file)
    print()
    
#addi_sql_list = ([
#                  "mod-mod.sql",
#                  "app.sql",
#                  "job-step-dataset.sql",
#                  "mod-dataset.sql",
#                  "mod-dbtable.sql",
#                  "screen-mod.sql",
#                  "trans-mod.sql",
# ])
