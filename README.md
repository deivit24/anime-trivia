## Anime Trivia

This is a test repo where I am building a anime database using web scrapping and dbt.

The goal is to host this in my raspberry pi and run a job that we scrapes MAL on a weekly basis, stores the raw data in postgres.

I then use dbt to transform the data into something more useful.

I am also testing a new JS Framework (I know... but this one is different) called VanJs. Which is a framework that does not use
jsx and it's less than 1kb.

The final thing that I need to do is host this super east client side app in my raspberry pi to see if it works.

## Environment setup

As you can see in the `docker-compose.yml` env files, there needs to be two env files created: `.env.dev` and `.env.prod`.

```shell
USERNAME=changeme
PASSWORD=somesuperstrongpassword
POSTGRES_HOST=changeme
POSTGRES_PORT=5432
POSTGRES_USER=changeme
POSTGRES_PASSWORD=changeme
POSTGRES_DB=changeme
POSTGRES_DRIVER=postgresql
```

These environment variables should encompass the `dev` and `prod` variables.

Please do the same for the `client` directory. This is needed for vite to pick up environment variables.

```shell
VITE_BASE_URL=http://localhost:8080/trivia
```

This should be all that is needed.

Then run `source start.sh dev`

This runs the necessary docker-compose commands for the environments.

## Client directory

I currently have a broken/barely working frontend. I am using the VanJS framework which uses vanilla JS hence the name.

I want to this to be a simple as possible. These are the requirements:

- User chooses a level
- Five questions get generated (this happens in the backend)
- When a question is answered, I want the question to be removed and a pop up appear. Like a message or banner that disappears.
  - I want to state whether the question was correct or wrong as well as a snarky comment
- At the end give them a score

### App directory

This holds the api which is fairly simple and the dbt project. I did this so my docker image can be used and there will be no need to create another one.

The dbt creates view based off of raw tables that was scrapped my anidb. Purpose is to have a table of all the anime and some useful attributes. Having a database like this can be very useful. The views that are created are anime, characters and character descriptions.

The api its self creates a query based on the arguments that were passed and generates 5 questions. A question contains an image (question) and 5 possible answers.

The level is based on popularity on the anime as well as well as most favorite/voted. Then we get a couple of characters from the anime and anime that is similar the generate the possible answers. The query is very very barebones and can be improved on.

## anime_scrapper

This has two versions. One scrapping data from anidb and the other is scrapping data from MAL. It generates a csv file that populates the raw tables.

# Reasons for doing this?

Main reason why I am doing in this is because I want to test hosting this on my Raspberry Pi. I feel like this project is a complicated enough to test
if it works. Then will tunnel this using Cloudfare. This way, I can start hosting all my projects on my raspberry pi.
