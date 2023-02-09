# test-project-api

> This is an api for a very simple version of the social network.

# Technologies

 - Django rest framefork
 - Celery
 - Redis
 - PostgreSQL
 - Docker
 - Dcoker-compose

# Build and Run
```
sudo docker-compose up --build 
```
      
# Migrate
```
# Stop stack
# Type this in work dir

sudo docker-compose run main_api python3 ./src/API/manage.py makemigrations api 
sudo docker-compose run main_api python3 ./src/API/manage.py migrate

# Start your stack
# Migration DONE :)
```

# ToDo


- [x] Build system with docker

- [x] User can register in system (Email activation)
- [x] User can log in/log out to the system (JWT token only)
- [x] User can change/reset password (Email)
- [x] User can create and edit own posts

    - [x] Create post
    - [x] Post all
    - [x] Post by id
    - [x] Update post data

- [x] User can see the posts from other users
- [ ] User can add and remove a like from users posts (except own)
- [ ] User can update own profile
- [ ] Add Search by post title
- [x] Connect swagger docs
- [ ] Flake8

# Bonus-meme ;)
![](data:image/jpeg;base64,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)