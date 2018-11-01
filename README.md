# Skate-Spotter-BE

Skate-Spotter-BE is an api that interacts with a database designed to store specific information for an app that allows skateboarders to share their favorite skate spots. The idea is that, architecturally, there are more fun places to skateboard and these places can now be shared across an online community.

[This link will take you to the front end page](https://github.com/brandonfiebiger/skateSpotter)

## EndPoints
#### *For Security reasons there is not a link to the deployed db but if you fork and clone this repo you can use these endpoints to create your own skate spot database api and even add more features as well

1. `/api/v1/spots`

   This endpoint gives you all the spots in the db.
2. `/api/v1/spots/:id`

   This endpoint gives you a single spot by spot id.
3. `/api/v1/skaters`

   This endpoint gives you all the skaterboarders in the db.
4. `/api/v1/skaters/:id`

   This endpoint gives you a single skateboarder by id.
5. `/api/v1/sign_up`

   This endpoint is for new user sign up.
      
         A user has:
            1.name
            2.email
            3.tag
            4.password
         These attributes have to be sent to this endpoint via a POST 
         
         and they need to be included in the body as JSON like so:
         { "name": "John Dude",
         "email": "john.dude@pmail.com",
         "tag": "rock and roll will never die!",
         "password": "skAterDood318"
         }
6. `/api/v1/login`
