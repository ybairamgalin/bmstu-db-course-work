#!/bin/bash
pgmigrate -t latest migrate &&
pgmigrate -t latest info > logs/migrate.log &&
echo 'Migrations were applied, service started' &&
uvicorn task_tracker_backend.main:task_tracker --host 0.0.0.0 --reload;
