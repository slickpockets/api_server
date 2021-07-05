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
        {"key": key, "value": value}
  delete: /_delete
    expect: {"key": key}
  
  key_access: /<key>
    expects: key exists otherwise errors, will route to correct endpoint

todo:
  redis:
    expand to multiple strings at once.
    lists
    sets
    hashes
    others
  postgres:
    connect to postgres
