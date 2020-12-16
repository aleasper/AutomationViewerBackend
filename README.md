# AutomationViewerBackend
Django application used as backend for AutomationViewer web-app

Actual API url: https://automation-viewer-backend.herokuapp.com/

## Routes:

### Access to 'ПАСИПМ' data
#### Route: `/vk_data`<br>
#### Supported methods:
GET
with query parameters:
<br>`app_id=<application id>`
<br>`login=<login>`
<br>`password=<password>`

Example: `https://automation-viewer-backend.herokuapp.com/vk_data?app_id=app_0&login=kseniya&password=123`

Success response:
```
{
    {
    "app_info": [
        {
            "_id": -158452705,
            "info": {
                "likes": 0,
                "comments": 0,
                "reposts": 0,
                "name": "<public name>"
            }
        },
        {
        ...
        }
    ],
    "ok": true
}
```
Error response:
```
{
    "error": {
        "msg": "<error message>",
        "code": <error code>
    },
    "ok": false
}
```

### Register user
#### Route: `/register`<br>
#### Supported methods:
POST
with body:
`{"login": "<login>", "password": "<password>"}`

Example: `https://automation-viewer-backend.herokuapp.com/register

Success response:
```
{
    "status": "registered",
    "ok": true
}
```
Error response:
```
{
    "error": {
        "msg": "already registered",
        "code": 101
    },
    "ok": false
}
```

### Check user registration / Login user
#### Route: `/login`<br>
#### Supported methods:
POST
with body:
`{"login": "<login>", "password": "<password>"}`

Example: `https://automation-viewer-backend.herokuapp.com/login

Success response:
```
{
    "status": "registered",
    "ok": true
}
```
Error response:
```
{
    "error": {
        "msg": "wrong login/password",
        "code": 4
    },
    "ok": false
}
```

####Error codes:
0 - Server error<br>
1 - Query parameter `app_id` is not specified<br>
4 - Wrong login/password in request<br>
101 - User already registered<br>

