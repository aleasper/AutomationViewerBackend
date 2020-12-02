# AutomationViewerBackend
Django application used as backend for AutomationViewer web-app

Actual API url: https://automation-viewer-backend.herokuapp.com/

## Routes:

### Access to 'ПАСИПМ' data
#### Route: `/vk_data`<br>
#### Supported methods:
`post` with body {'app_id' : '<ПАСИПМ application id>'}