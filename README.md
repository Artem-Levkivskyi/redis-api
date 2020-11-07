# REDIS API. Service for work with REDIS by DRF.
## Functional:
### You can use next DRF requests:
* POST - for add new value to REDIS storage.
* GET - for get list of values in REDIS storage.
* GET - for get value in REDIS storage by entered in request key.
* DELETE - for delete some value in REDIS storage by entered in request key.
---
## How it work:
### Work with single item in REDIS storage:
* For get value from REDIS you should send GET-request to like this - website.host/api/items/{mykey}, where 'mykey' - key for your value.
* For delete value from REDIS you should send DELETE request with key of your value.
### Work with all items in REDIS storage:
* For get values from REDIS you should send GET-request like this - website.host/api/items.
* If you want create new record in REDIS storage, you should send POST-request with key-value object to 127.0.0.1:8000/api/items.
