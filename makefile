.PHONY: unit-test
unit-test:
	pytest tests/unit --cov=zombie_nomnom_api --cov-report=term --cov-report=xml --cov-report=html --html=htmlcov/report.html
.PHONY: int-test
int-test:
	pytest tests/integration --cov=zombie_nomnom_api --cov-report=term --cov-report=xml --cov-report=html --html=htmlcov/report.html
.PHONY: all-test
all-test:
	pytest tests --cov=zombie_nomnom_api --cov-report=term --cov-report=xml --cov-report=html --html=htmlcov/report.html
.PHONY: db-test
db-test:
	pytest tests -m mongo --cov=zombie_nomnom_api --cov-report=term --cov-report=xml --cov-report=html --html=htmlcov/report.html
.PHONY: docs
docs:
	pdoc ./zombie_nomnom_api
.PHONY: build-pdocs
build-pdocs:
	pdoc ./zombie_nomnom_api -o ./docs
.PHONY: build-docs
build-docs:
	make cov-all
	make build-pdocs
.PHONY: serve-docs
serve-docs:
	python -m http.server -d docs 8080
.PHONY: cov-all
cov-all:
	pytest tests --cov=zombie_nomnom_api --cov-report=html:docs/coverage --html=docs/coverage/report.html
.PHONY: render-cov
render-cov:
	python -m http.server -d htmlcov 8081
.PHONY: format
format:
	black .
.PHONY: install
install:
	pip install . -r requirements-dev.txt
.PHONY: lint
lint:
	black . --check
.PHONY: package
package:
	ytt -f deployment/lib/schema.yaml -f deployment/envs/${ENVIRONMENT}/values.yaml -f deployment/deployment.yaml -f deployment/ingress.yaml -f deployment/namespace.yaml -f deployment/service.yaml > zombie-nomnom-api-${ENVIRONMENT}.yaml
.PHONY: ensure-resources
ensure-resources:
	docker compose up mongo -d || echo "Mongo is already running"