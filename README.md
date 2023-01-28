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
# Build and run stack
# Type this in work dir

sudo docker-compose run main_api python3 ./src/API/manage.py migrate

# Restart your stack
# Migration DONE :)
```

# ToDo


- [x] Build system with docker

- [ ] User can register in system (Email activation)
- [x] User can log in/log out to the system
- [ ] User can change/reset password (Email)
- [ ] User can create and edit own posts
- [ ] User can see the posts from other users
- [ ] User can add and remove a like from users posts (except own)
- [ ] User can update own profile
- [ ] Add Search by post title
- [ ] Connect swagger docs
- [ ] Flake8


