# StorylyAPI
I utilized [django-ninja framework](https://django-ninja.rest-framework.com) that goe together with Django to provide with a FastAPI style interface to REST API developing. Open API documentation for the challenge is available at [openapi docs](http://127.0.0.1:8000/api/v1/docs/), also a list of postman requests I tested is also available in the project.

Project uses a redis cache container as well as an internal sqlite instance for db storage that is supported by django-ninja. StorylyAPI is also dockerized and will work as a standalone app using the command ```docker-compose up```. 

Sample data I used in the application is in ```stories/data/sample_stories.json``` which I use a migration script to migrate to the db at startup.

I also wrote integration tests for the api which runs when creating the docker-compose.

For manual startup run 
```
sh -c "python manage.py makemigrations &&
       python manage.py migrate &&
       python manage.py ingest_stories &&
       python manage.py test &&
       python manage.py runserver 0.0.0.0:8000"
```

# Apache AB Testing 
Having dockerized the full application I started it using docker-compose.
```
(venv) (base) ➜  storylyapi git:(main) docker-compose up -d
Starting storylyapi_redis-server_1 ... done
Recreating storylyapi_web_1        ... done
```

After which I run an apache ab test for 200 requests with 100 concurrency (max my system allowed) on the endpoint that does not use any explicit caching. <br><br>

```
(venv) (base) ➜  storylyapi git:(main) ✗ ab -c 100 -n 200 "http://localhost:8000/api/v1/stories/1"
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Finished 200 requests


Server Software:        WSGIServer/0.2
Server Hostname:        localhost
Server Port:            8000

Document Path:          /api/v1/stories/1
Document Length:        47 bytes

Concurrency Level:      100
Time taken for tests:   3.208 seconds
Complete requests:      200
Failed requests:        0
Total transferred:      67200 bytes
HTML transferred:       9400 bytes
Requests per second:    62.35 [#/sec] (mean)
Time per request:       1603.883 [ms] (mean)
Time per request:       16.039 [ms] (mean, across all concurrent requests)
Transfer rate:          20.46 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2   1.6      0       4
Processing:    42  793 930.0    117    3168
Waiting:       35  787 931.2    108    3168
Total:         43  795 931.2    118    3172
WARNING: The median and mean for the initial connection time are not within a normal deviation
        These results are probably not that reliable.

Percentage of the requests served within a certain time (ms)
  50%    118
  66%   1162
  75%   1358
  80%   1536
  90%   1987
  95%   2805
  98%   3168
  99%   3169
 100%   3172 (longest request)
 ```

I reset using ```docker-compose down``` to stop the application, and restart. Results for the cached endpoint are: <br><br>

```
(venv) (base) ➜  storylyapi git:(main) ✗ ab -c 100 -n 200 "http://localhost:8000/api/v1/stories/cached/1"
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Finished 200 requests


Server Software:        WSGIServer/0.2
Server Hostname:        localhost
Server Port:            8000

Document Path:          /api/v1/stories/cached/1
Document Length:        47 bytes

Concurrency Level:      100
Time taken for tests:   2.783 seconds
Complete requests:      200
Failed requests:        0
Total transferred:      67200 bytes
HTML transferred:       9400 bytes
Requests per second:    71.87 [#/sec] (mean)
Time per request:       1391.490 [ms] (mean)
Time per request:       13.915 [ms] (mean, across all concurrent requests)
Transfer rate:          23.58 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.2      2       3
Processing:    38  711 793.6    118    2743
Waiting:       35  704 795.3    110    2743
Total:         38  712 794.5    118    2746

Percentage of the requests served within a certain time (ms)
  50%    118
  66%   1094
  75%   1276
  80%   1460
  90%   1880
  95%   2713
  98%   2740
  99%   2744
 100%   2746 (longest request)
 ```

 We observe a speedup on the endpoint that utilizes caching.

<br> <br>

# Approach for Bonus Assignment - Calculating DAU
I didn't have time to implemet this solution but to solve it I would have used kafka streams and cron jobs that aggregate the batches to the count periodically. As event counts do not need to be highly accurate cron jobs that run aggregations on kafka streams would suffice.
These features are supported in [faust](https://faust.readthedocs.io/en/latest/).
