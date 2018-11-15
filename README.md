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

   This endpoint is for login after a user has signed up.
   
         To login in the user provides their name and password which are
         to this endpoint via a POST and are included in the body as JSON like so:
         
            { "name": "John Dude",
            "password": "skAterDood318"
            }
7. `/api/v1/skater_page`

   This endpoint serves the specific user information for a user logged in
   if a user tries to access this page without logging in an error is sent.
   
8. `/api/v1/update_skater`
  
   This is the update user endpoint where a user can change their information.
   The form on the front end will have to be populated with the user's current
   information to avoid any empty values the user doesn't supply.
   
         These attributes have to be sent to this endpoint via a PATCH 
         and they need to be included in the body as JSON like so:
         
            { "name": "John Dude the Second",
            "email": "john.dude@pmail.com",
            "tag": "rock and roll will never die ever!",
            "password": "skAterDood318"
            }
            
9. `/api/v1/new_spot`

   This endpoint is where the user submits a new skateboarding spot. A new spot cannot be
   created unless a user is signed in. When A new spot is created by a signed in user their
   user id is associated with that spot created.
   
         These attributes have to be sent to this endpoint via a POST 
         and they need to be included in the body as JSON like so:
         
         {"name": "The stairs in the park",
         "description": "10 steps with a clear landing at the bottom",
         "latitude": 33.123123,
         "longitude": 133.123123,
         "photo_url": "www.someurlforajpeg.com"
         }
         
         *This api was designed to work with a React Native front end application
         which sends latitude and longitude coordinates from the mobile device of 
         the user, assuming the user is at the specific skate spot when they submit.
         
10. `/api/v1/update_spot/:id`

   This endpoint is for updating a spot, the spot's id has to be supplied in the url. 
   As with submitting a new spot, the user has to be logged in and is only able to 
   update those spots that are associated with their user id.
   
         These attributes have to be sent to this endpoint via a PATCH 
         and they need to be included in the body as JSON like so:
         
         {"name": "The stairs in the park by the church",
         "description": "10 steps with a clear landing at the bottom",
         }
         
11. `/api/v1/delete_spot/:id`

   This is an endpoint to delete a spot. A spot can only be deleted by a user
   who is logged in and who has created that spot. The spot id has to be included
   in the url and the http verb DELETE has to be specified.
   
12. `/api/v1/logout`

   This endpoint logs out the user from the back end but the browser of the front end app
   has to be uncached or the cookie it has still stored will confuse the backend app.
   
   the cookie stored will confuse the 

   This endpoint logs out the user 
