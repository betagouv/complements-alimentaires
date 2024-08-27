#!/bin/bash
curl $S3CFG_FILE_URI > ~/.s3cfg
# retrieve most recent date
FILEPATH=$(s3cmd ls s3://csv-data| tail -1 | awk '{ print $2 }')
DATE=${FILEPATH##"s3://csv-data/"}
DATE=${DATE%"/"}
mkdir csv-data
# if this date doesn't exist yet
if ls csv-data/$DATE ; then
    echo "This data has already been loaded"
else
    # retrieve most recent files
    mkdir csv-data/$DATE/
    s3cmd get s3://csv-data/$DATE/ --recursive csv-data/$DATE/
    # import those files to database (django models)
    python $APP_ID/manage.py load_ingredients -d csv-data/$DATE $DATE
fi
