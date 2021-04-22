# Rover Coding Project

## Requirement
Python Version: 3.7

pandas == 0.25.3


## Running
To run the code, please move to the directory where you saved the "reviews.csv" file, and run:
```
python3 SearchRanking.py ./reviews.csv
```
The program will output a "sitter.csv" in the same directory.

## Discussion Question
- What infrastructure choices might you make to build and host this project at scale? Suppose your web application must return fast search results with a peak of 10 searches per second. 

To scale up the web application, we can utilize load balancers to distributes client requests efficiently across multiple servers. On the top of that, we can cache the user's searching requests by implementing message queue and Redis.