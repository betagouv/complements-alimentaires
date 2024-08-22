curl $S3CFG_FILE_URI > .s3cfg
# retrieve most recent date
FILEPATH=$(s3cmd ls s3://csv-data| tail -1 | awk '{ print $2 }')
DATE=${FILEPATH##"s3://csv-data/"}
DATE=${DATE%"/"}
# retrive most recent files
mkdir -p csv-data/$DATE/
s3cmd get s3://csv-data/$DATE/ --recursive csv-data/$DATE/
# import those files to database (django models)
python $APP_ID/manage.py load_ingredients -d csv-data/$DATE $DATE
