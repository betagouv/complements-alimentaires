## Instruction pour la migration des données de WSSQL à la BDD Compl'Alim

1. Create all table in psql
2. Convert all UTF-16 files to UTF-8 and transform "" to empty fields
~~~
for f in *.csv; do iconv -f UTF-16 -t UTF-8 "$f" | sed 's/""//g' > "${f%.*}_utf8.csv" ; done
~~~
3. Copy all data from csv with
~~~
for f in *_utf8.csv; do
    table_name=${f%_utf8.csv}
    echo "-> Import des données de $f"
    psql postgresql://<user>:<passwd>@<ip>:<port>/<database>  -c "\copy $table_name from $f delimiter ',' csv header;";
done
~~~


4. Execute migration scripts in shell
~~~
from data.etl.teleicare_history.extractor import match_companies_on_siret_or_vat, create_declarations_from_teleicare_history
match_companies_on_siret_or_vat()
create_declarations_from_teleicare_history()
~~~
