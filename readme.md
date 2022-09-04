# Mountain Pass API (SF 09.2022)

API for submitting mountain pass data

* FastAPI
* BeanieODM
* MongoDB
* Motor

## API Methods

`GET '/submitData/{id}'`

Returns mountain pass data by its ID

`GET /submitData?user__email={email}`

Return list of mountain pass data submitted by user with given email

`POST /submitData`

Save new mountain pass data to DB

`PATCH /submitData/{id}` 

Edit existing mountain pass data