# Log analysis

## Project description
This project is a reporting tool that answers some questions. It's build in Python and uses the **psycopg2** library to access the database.

This are the questions to be answered:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Setup Postgres and database

In this guide i'll use Postgres on same machine not using VM

To install Postgres i followed this tutorial by [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04).

With Postgres server installed you will need to setup the database.
### On the PSQL CLI:
```
CREATE DATABASE news;
```
Quit the PSQL CLI with the following command or by `Ctrl+d`
```
\q
```
Now that you created the database you need to recover the data from de dump file

Download the dump file [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
Extract the file and on Terminal change to the extracted file folder and run this 
```
psql -d news -f newsdata.sql
```
### Congratulaitons! You have recovery the data

## To run this project you just need to run with Python3
```
python3 log-analysis.py
```
## Expected output
```
1. What are the most popular three articles of all time?

Candidate is jerk, alleges rival — 338,647 views.
Bears love berries, alleges bear — 253,801 views.
Bad things gone, say good people — 170,098 views.


2. Who are the most popular article authors of all time?

Ursula La Multa — 507,594 views.
Rudolf von Treppenwitz — 423,457 views.
Anonymous Contributor — 170,098 views.
Markoff Chaney — 84,557 views.


3. On which days did more than 1% of requests lead to errors?

2016-07-17 — 2.27% errors.
```
