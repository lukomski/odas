# odas

## Run project
```
docker-compose up --build
```
open [http://localhost:8081](http://localhost:8081)

## Planned enpoints

#### /api/user

`GET`  

base info about current user based on cookies

`POST` ?username=,password= 

authorize, create session 

#### /api/users
`GET`                   

get list of users

`POST`?username=,password=

add new user

#### /api/users/<user_id>/password
`PUT` ?password=

change password for current user

#### /api/notes
`GET`?userId=

notes filterd by userId if set

`POST`?title=,message=,viewers=[],public

add new note for current user

#### /api/notes/<note_id>
`GET`

info about the note

`DELETE`

delete note

#### /api/notes/<note_id>/title
`POST`?title=

update title of the note

#### /api/notes/<note_id>/message
`POST`?message=

update message of the note

#### /api/notes/<note_id>/viewers
`POST`?userIds=[],public=

update viewers of the note  
