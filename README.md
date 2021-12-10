# xeneta

## DB Schema
![image](https://user-images.githubusercontent.com/26124346/145563288-cdf61869-2350-43be-ace3-97dc9638568e.png)

 Updated dbschema, created a new table named port_region where all ports and their related regions are stored.

## Installation steps
`cd xeneta/`

`docker-compose up -d --build`

## Test
Log in to the container

`docker exec <container_id> /bin/sh`

`python manage.py test --keepdb`

To get test coverage

`coverage run manage.py test --keepdb`

`coverage report`
