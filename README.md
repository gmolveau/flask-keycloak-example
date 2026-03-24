# A simple example of a preloaded keycloak and a flask app

- `docker` is required
- `just` is required : <https://github.com/casey/just>
- a `keycloak` instance will be preloaded with 2 users and 2 groups
  - `user:user` in group `developers` with role `read_only`
  - `admin:admin` in group `sysadmins` with role `full_access`

## Getting started

In terminal 1 :

- `just run-keycloak`

go to <http://localhost:8080> and login with `keycloak:keycloak` to check that it works

In terminal 2 :

- `uv sync`
- `just run-flask`

go to <http://localhost:8000> and login with `user:user` or `admin:admin`

the username, sub, roles and groups should be printed
