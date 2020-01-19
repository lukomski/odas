## Endpoints

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

`POST`?title=,message=,viewers=[],public

update note for current user

`DELETE`

delete note
