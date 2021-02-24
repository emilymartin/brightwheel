README:
Emily Martin
2/24/2021
Brightwheel interview

How to install/run your service:

1. Download the repo from gitlab
In terminal:
2. Cd into brighwheel directory
2. Run python setup.py install
3. Run python -m interview
4. Run unit test by using the command pytest

Output:
(Sorry it prints a lot of warnings at the beginning)
1. First 10 lines of the data frame
2. The shape of the final data frame


Which language, framework and libraries you chose and why?

I chose python because it's what I use most often and am most familiar with.

I saved functions to pull data from the three sources in file in the sources folder. I got in the habit of doing this incase I need to pull these sources for other ETLs in the future.

I have a main file that calls get_providers in the providers file. In that file is where I join and clean all the data. 

I saved a test for clean_emails in the tests folder. I like to keep all my tests in one place as my repos get bigger.


Libraries:
requests: so I can get data from the APIs
re: so I could search the html text for the number of total pages in the OMCC database


I made a few assumptions for this data:
- I assumed the internal API data is most up to date, followed by the OMCC provider database, then the attached CSV.


Tradeoffs - 

1. There are definitely some checks I would have liked to add, which I just didn't get to. Inside the get_provider_data function, I would like to make sure we actually get data back from the interview_sources functions before joining, This would make my code a little more robust in case

2. I don't actually dump the data into a Postgres data base. I'm not entirely sure how to do that and send it to you so it works. And I didn't have time to figure it out. (I do know know to dump data frames into Postgres in my own environment and am happy to show you later if you need me to.)

3. I only unit tested the clean_email function, I ran out of time so I didn't get a chance to test the clean_providers function.

4. All columns are strings

5. I also ran out of time before I finished linting everything. I tried to keep it as neat as possible. But linting definitely makes it better

6. You said limit this to 2 hours, so I want to be very candid about where I went over and fair to other candidates and your interview process. I had never pulled a table from the internet that was in HTML before. This took me about 2 hours to figure out on it's own. Aside from that one piece, I completed the rest of this within the 2 hours. I really wanted to be able to do the analysis with all the data, since that's the part I'm actually good at. 


SQL Queries:
I have them here since I don't save the final data frame in a table.

1. select count(provider_name) from all_providers
    where type_of_care = 'Family Child Care Home'

This gives me 643 Family Child Care Home providers

2. select zip, count(provider_name) from all_providers
    where zip is not Null
    group by zip
    order by count desc
    limit 1
I get 28 providers in zip code 92124
