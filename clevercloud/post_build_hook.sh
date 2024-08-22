curl $S3CFG_FILE_URI > .s3cfg
# retrieve most recent date
FILEPATH=$(s3cmd ls s3://csv-data| tail -1 | awk '{ print $2 }')
DATE=${FILEPATH##"s3://csv-data/"}
DATE=${DATE%"/"}
# retrive most recent files
s3cmd get s3://csv-data/$DATE/ --recursive
# import those files to database (django models)
python manage.py load_ingredients
