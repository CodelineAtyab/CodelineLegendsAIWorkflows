#!/bin/sh
# Create the Temporal + visibility databases and apply schema migrations.
# Idempotent: safe to run on every container start and on version upgrades.
set -eu

: "${POSTGRES_SEEDS:?POSTGRES_SEEDS is required}"
: "${POSTGRES_USER:?POSTGRES_USER is required}"
: "${POSTGRES_PWD:?POSTGRES_PWD is required}"

DB_PORT="${DB_PORT:-5432}"
DBNAME="${DBNAME:-temporal}"
VISIBILITY_DBNAME="${VISIBILITY_DBNAME:-temporal_visibility}"
SQL_PLUGIN="${SQL_PLUGIN:-postgres12}"
CONNECT_TIMEOUT="${CONNECT_TIMEOUT:-60}"

# temporal-sql-tool picks the password up from SQL_PASSWORD / PGPASSWORD.
export SQL_PASSWORD="${SQL_PASSWORD:-$POSTGRES_PWD}"
export PGPASSWORD="${PGPASSWORD:-$POSTGRES_PWD}"

SCHEMA_ROOT="/etc/temporal/schema/postgresql/v12"

sql_tool() {
  db="$1"
  shift
  temporal-sql-tool --plugin "$SQL_PLUGIN" \
    --ep "$POSTGRES_SEEDS" -p "$DB_PORT" -u "$POSTGRES_USER" \
    --db "$db" "$@"
}

wait_for_postgres() {
  attempt=1
  while ! nc -z -w 5 "$POSTGRES_SEEDS" "$DB_PORT"; do
    if [ "$attempt" -ge "$CONNECT_TIMEOUT" ]; then
      echo "ERROR: PostgreSQL not reachable at ${POSTGRES_SEEDS}:${DB_PORT} after ${CONNECT_TIMEOUT} attempts" >&2
      exit 1
    fi
    echo "Waiting for PostgreSQL at ${POSTGRES_SEEDS}:${DB_PORT} (attempt ${attempt}/${CONNECT_TIMEOUT})..."
    attempt=$((attempt + 1))
    sleep 2
  done
  echo "PostgreSQL is reachable."
}

# create_db <name> <schema-path>
create_db() {
  db="$1"
  schema_path="$2"

  echo "Ensuring database '${db}' exists..."
  if sql_tool "$db" create >/tmp/sql-create.log 2>&1; then
    echo "Database '${db}' created."
  elif grep -qi "already exists" /tmp/sql-create.log; then
    echo "Database '${db}' already exists."
  else
    cat /tmp/sql-create.log >&2
    echo "ERROR: failed to create database '${db}'" >&2
    exit 1
  fi

  echo "Applying base schema to '${db}'..."
  sql_tool "$db" setup-schema -v 0.0

  echo "Applying schema migrations to '${db}'..."
  sql_tool "$db" update-schema -d "${SCHEMA_ROOT}/${schema_path}/versioned"
}

wait_for_postgres

create_db "$DBNAME" "temporal"
create_db "$VISIBILITY_DBNAME" "visibility"

echo "Temporal schema setup complete."
