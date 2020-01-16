PATH=C:/Program Files/PostgreSQL/11/

PGPASSWORD=dbpassword0000001
export PGPASSWORD
pathB=C:/Users/Alina/backup
dbUser=alina
database=store

find $pathB 
pg_dump -U $dbUser $database | gzip > $pathB/pgsql_$(date "+%Y-%m-%d").sql.gz

unset PGPASSWORD