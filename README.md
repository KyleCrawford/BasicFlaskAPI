# BasicFlaskAPI
A Simple Python Flask REST API

This application is a simple Python Flask Application with a few simple endpoints.
The program is meant to simulate a blog type application, and uses an API from Hatchways 

Endpoints 

  /api/ping  
    Returns 'success: true' if the app is running properly.  
  
  /api/posts  
    parameters:   
    &ensp  tags - mandatory, the type of posts to return (the tags represent the 'type' of the post).  
   &ensp   sortBy - optional, what field to sort the data by. Options include id, reads, likes, popularity.  
  &ensp    direction - optional (default descending), the direction of the data to be ordered.   
  
  All data returned is in JSON format
