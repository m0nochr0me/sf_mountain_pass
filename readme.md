# Mountain Pass API (SF 09.2022)

API for submitting mountain pass data

* FastAPI
* BeanieODM
* MongoDB
* Motor

## API Methods

`GET '/submitData/{id}'`

Returns mountain pass data by its ID

`POST /submitData`

Save new mountain pass data to DB

`PATCH /submitData/{id}` 

Edit existing mountain pass data