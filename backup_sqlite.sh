#!/bin/bash

# Caminhos
DATA=$(date +%Y-%m-%d_%H-%M)
DB_PATH="/home/hidromosaic/App_mosaic/db.sqlite3"
BACKUP_DIR="/home/hidromosaic/backups"

# Cria pasta se não existir
mkdir -p $BACKUP_DIR

# Cópia do banco
cp $DB_PATH $BACKUP_DIR/db_backup_$DATA.sqlite3

# Remover backups com mais de 7 dias
find $BACKUP_DIR -type f -name "*.sqlite3" -mtime +7 -delete