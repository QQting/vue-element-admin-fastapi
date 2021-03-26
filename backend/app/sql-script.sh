#!/bin/bash

if [ "$1" = "drop" ]; then
  echo "drop existed database"
  sudo -u postgres dropdb ADLINK-DB
  sudo -u postgres dropuser ros
  rm -rf alembic/versions/*
fi

if [ "$1" = "new" ]; then
  echo "create new database"
  sudo -u postgres createuser ros -P
  sudo -u postgres createdb ADLINK-DB
fi

