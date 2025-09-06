####

# 🗳️ Election API

A scalable and secure backend API built with Django and Django REST Framework for managing electoral systems. Supports candidate registration, voter authentication, voting, and result aggregation.

---

## Features

- Candidate CRUD operations
- Voter registration and login
- Secure vote casting
- Real-time result tallying
- Role-based permissions
- Token-based authentication
- Robust error handling and validation

---

## 📘 API Endpoints

## Voter Registration
POST/Elections/register/
{
    "email": "gareth@gmail.com",
    "password" : "2345",
    "national_id" : "2123",
    "age" : "40"

}
{
    "email": "cedy@gmail.com",
    "password" : "200",
    "national_id" : "1",
    "age" : "40"

}
GET/Elections/register
{
    "email" : "gareth@gmail.com"
    "national_id" : "2123"

}
## Candidate Registration
GET/Elections/candidates/
{
    "name" : "Khal Drogo"
    "party" : "Valhalla"

}
{
    "name" : "Candidate B"
    "party" : "Valhalla"

}
POST/Elections/candidates/
{
    "id" : "6",
    "name" : "Jessy",
    "party" : "roots"
    
}
{
    "id" : "3"
    "name" : "Khal Drogo"
    "party" : "Valhalla"

}
{
    "id" : "4"
    "name" : "Candidate B"
    "party" : "Valhalla"

}
### 🔐 Authentication

#@loginrequired
## voting 
POST/Elections/Vote/1/
    {
        "voter" : : "2123",
        "candidate" : "Khal Drogo"
    }

    {
        "voter": 1,
        "candidate": "Candidate A"
    },
    {
        "voter": 2,
        "candidate": "Candidate B"
    }

## results
GET/Elections/Candidate/4/
{
    "id" : "4"
    "name" : "Candidate B"
    "party" : "Valhalla"

}
## Status Code     	Meaning
1. 200                 OK Successful ly retrieved 
2. 201                 Created recorded successfully
3. 400                 Bad Request	Invalid data
4. 401                 Unauthorized	    Authentication required
5. 404                 Not Found	not found

####