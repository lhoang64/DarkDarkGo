#!/bin/bash
#    import.sh: Automate script for importing data to mgmt_db
#    Author: Hoanh An (hoanhan@bennington.edu)
#    Date: 12/2/17

echo "==============================================================="
echo "* BEGINNING DATA IMPORT PROCESS                               *"
echo "---------------------------------------------------------------"
echo "* >> Ensure mgmt_db exists and is owned by `whoami` <<        *"

echo "---------------------------------------------------------------"
echo "* CREATING SCHEMA                                             *"
echo "---------------------------------------------------------------"
psql mgmt_db < mgmt_schema.sql

echo "---------------------------------------------------------------"
echo "* IMPORTING host TABLE                                        *"
echo "---------------------------------------------------------------"
psql mgmt_db < host.sql

echo "---------------------------------------------------------------"
echo "* IMPORTING LINK TABLE                                        *"
echo "---------------------------------------------------------------"
psql mgmt_db < link.sql

#echo "---------------------------------------------------------------"
#echo "* IMPORTING CHUNK TABLE                                       *"
#echo "---------------------------------------------------------------"
#psql mgmt_db < chunk.sql
#
#echo "---------------------------------------------------------------"
#echo "* IMPORTING CRAWLER TABLE                                      *"
#echo "---------------------------------------------------------------"
#psql mgmt_db < crawler.sql
#
#echo "---------------------------------------------------------------"
#echo "* IMPORTING INDEX BUILDER TABLE                                *"
#echo "---------------------------------------------------------------"
#psql mgmt_db < index_builder.sql
#
#echo "---------------------------------------------------------------"
#echo "* IMPORTING INDEX SERVER TABLE                                 *"
#echo "---------------------------------------------------------------"
#psql mgmt_db < index_server.sql

echo "---------------------------------------------------------------"
echo "* ADDING FOREIGN KEY CONSTRAINTS                              *"
echo "---------------------------------------------------------------"
psql mgmt_db < add_constraints.sql

echo "---------------------------------------------------------------"
echo "* CREATING INDEXES                                            *"
echo "---------------------------------------------------------------"
psql mgmt_db < create_indexes.sql

echo "---------------------------------------------------------------"
echo "* IMPORT PROCESS COMPLETE mgmt_db READY FOR USE!              *"
echo "==============================================================="