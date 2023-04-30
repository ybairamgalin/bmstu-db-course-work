
.PHONY : docker-up
docker-up : setup docker-build docker-compose.yaml
	docker compose up --detach

.PHONY : docker-up-v
docker-up-v : setup docker-build docker-compose.yaml
	docker compose up

.PHONY : docker-down
docker-down :
	docker compose stop

.PHONY : docker-restart
docker-restart :
	docker compose stop
	docker compose up

.PHONY : docker-build
docker-build : task_tracker_backend/Dockerfile
	docker compose build

.PHONY : setup
setup :
	mkdir -p logs
	mkdir -p logs/backend

.PHONY : test-backend
test-backend :
	pytest -vv testsuite/;

.PHONY : lint
lint : *.py
	pylint --rcfile=pylintrc $(git ls-files '*.py')

.PHONE : migrate
migrate :
	pgmigrate -t latest migrate;
	pgmigrate -t latest info;
