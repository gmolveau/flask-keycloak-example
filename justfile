set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

run-flask:
    uv run python3 app.py

run-keycloak:
    docker run --rm -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin -v ./keycloak/realm-export.json:/opt/keycloak/data/import/realm-export.json quay.io/keycloak/keycloak:24.0.0 start-dev --import-realm
