api server

connects to Redis instance.
expects the following environ vars:
REDISURL=
REDISPORT=
REDISDB=
REDISPASS=

api server:
  get: /string/<string>
    returns value for string
  post: /string/<string>
    expects string and value args:
        {"string": string, "value": value}


todo:
  redis:
    expand to multiple strings at once.
    lists
    sets
    hashes
    others
  postgres:
    connect to postgres
