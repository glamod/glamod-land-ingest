# Generating SQL scripts to load the Land observations

Generate a set of all the PSV Header Table files:

 write-fixed-headers-dirs.sh  

Which writes:

 beta_fix7_header_dirs.txt   

Then run a script to batch submit to LOTUS:

 submit-sql-creators.sh  

Which wraps:

 wrap-create-sql.sh     

Which in turn wraps:

 create-sql.py

