# powertofly-crawler

## Crawling method
When it's executed, crawling the published work within the range according to the time parameter. 

Get the job details after obtaining the job ID from the job list, and then save it in a json file.

## How to use
`docker build -t crawler .`

`docker run -it crawler ./bin/crawler/main.py 20210710 20210711`

OR

`python3 ./bin/crawler/main.py`

## Challenge
