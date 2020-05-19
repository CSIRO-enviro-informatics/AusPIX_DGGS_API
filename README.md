# AusPIX DGGS API
Web API wrapper for the AusPIX_DGGS https://github.com/GeoscienceAustralia/AusPIX_DGGS/

## Build

### docker-compose 

The following will build and run via docker-compose in a single step.
Note: Requires docker-compose and docker

```
$ docker-compose up -d
```

The API should be running on http://localhost:3000

Access API Doc at http://localhost:3000/api/doc/

### docker

Build and run using just docker as per below.
Note: Requires docker

```
$ docker build --tag auspixdggs:0.1 .
$ docker run -p 3000:3000 -d --name auspixdggs auspixdggs:0.1
```

The API should be running on http://localhost:3000/

Access API Doc at http://localhost:3000/api/doc/
