## Useful commands

### Start the database

```bash
bash scripts/start.sh
```

### Go inside the database

```bash
psql -h db -p 5432 -U postgres -d db
```

### Go inside the api container

```bash
docker exec -it independentstudy-api-1 /bin/bash
```

### Number of entries in each table

```bash
SELECT COUNT(*) FROM independent_study;
SELECT COUNT(*) FROM vector_embedding;
```

### Count rows in all tables

```sql
SELECT 
    table_name, 
    (xpath('/row/cnt/text()', xml_count))[1]::text::int as row_count
FROM (
    SELECT 
        table_name, 
        table_schema, 
        query_to_xml(format('SELECT COUNT(*) as cnt FROM %I.%I', table_schema, table_name), false, true, '') as xml_count
    FROM information_schema.tables
    WHERE table_schema = 'public'
) t
ORDER BY table_name;
```

### Count NULL values for each column

```sql
SELECT 
    table_name,
    column_name,
    COUNT(*) as total_rows,
    COUNT(*) FILTER (WHERE value IS NULL) as null_count,
    COUNT(*) FILTER (WHERE value IS NOT NULL) as non_null_count
FROM (
    SELECT 
        c.table_name,
        c.column_name,
        format('SELECT %I as value FROM %I', c.column_name, c.table_name) as query
    FROM information_schema.columns c
    WHERE c.table_schema = 'public'
) as q
CROSS JOIN LATERAL (
    SELECT value FROM dblink('dbname=db', q.query) AS t(value text)
) as data
GROUP BY table_name, column_name
ORDER BY table_name, column_name;
```

### Check table storage sizes

```sql
SELECT
    table_name,
    pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as total_size,
    pg_size_pretty(pg_table_size(quote_ident(table_name))) as table_size,
    pg_size_pretty(pg_indexes_size(quote_ident(table_name))) as index_size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC;
```

### Backup entire database

```bash
# Run these commands from your host machine
docker exec independentstudy-db-1 bash -c 'pg_dump -U postgres -d db > /tmp/backup.sql'
docker cp independentstudy-db-1:/tmp/backup.sql ./backup.sql
```

### Create database based on backup

```bash
# First, copy the backup file into the container
docker cp ./backup.sql independentstudy-db-1:/tmp/backup.sql

# Then restore the database
docker exec independentstudy-db-1 bash -c 'psql -U postgres -d db < /tmp/backup.sql'
```