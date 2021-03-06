### Register

Request to `/register`
```json
{
    "email": "user@mail.com",
    "password": "myPassword",
}
```

Response from `/register`
```json
{
    "status": "success",
    "token": "a665a4592042",
    "errors": [],
}
```

### Login

Request to `/login`
```json
{
    "email": "user@mail.com",
    "password": "myPassword",
}
```

Response from `/login`
```json
{
    "status": "success",
    "token": "a665a4592042",
    "errors": [],
}
```

### Execute

Request to `/execute/command/?text=hello&other_argument=whatever`
```json
{
    "token": "a665a4592042"
}
```

Response from `/execute/command/?text=hello&other_argument=whatever`
```json
{
    "status": "success",
    "message": "Hello",
    "details": {
        "full response": "Hello",
    },
    "errors": [],
}
```

### List all configs

Request to `/list-config`
```json
{
    "token": "a665a4592042"
}
```

Response from `/list-config`
```json
{
    "status": "success",
    "global config": {
        "city": "Sofia",
    },
    "user config": {
        "google api key": "653a665a45a665a45",
        "city": "London",
    },
    "errors": [],
}
```

### Set config

Request to `/set-config?key=city&value=Sofia`
```json
{
    "token": "a665a4592042"
}
```

Response from `/set-config?key=city&value=Sofia`
```json
{
    "status": "success",
    "errors": [],
}
```

### Get config

Request to `/get-config?key=city`
```json
{
    "token": "a665a4592042"
}
```

Response from `/get-config?key=city`
```json
{
    "status": "success",
    "global config": {
        "city": "Sofia",
    },
    "user config": {
        "city": "London",
    },
    "errors": [],
}
```
