#!/bin/bash
curl $S3CFG_FILE_URI > ~/.s3cfg
# retrieve most recent date
FILEPATH=$(s3cmd ls s3://csv-data| tail -1 | awk '{ print $2 }')
DATE=${FILEPATH##"s3://csv-data/"}
DATE=${DATE%"/"}
mkdir csv-data
# if this date doesn't exist yet
LAST_DATE=$(psql postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME -t -1 -c "select * from data_last_import order by import_date desc limit 1;")
if [[ "$LAST_DATE" == *"$DATE"* ]] ; then
    echo "This data has already been loaded"
else
    # retrieve most recent files
    mkdir csv-data/$DATE/
    s3cmd get s3://csv-data/$DATE/ --recursive csv-data/$DATE/
    # import those files to database (django models)
    python ~/$APP_ID/manage.py load_ingredients -d csv-data/$DATE $DATE
    psql postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME -c "insert into data_last_import (import_date) values ('$DATE');"
fi
