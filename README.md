# Backend Task Challenge

## Intro

The objective here is to assess usage of Python, Django and DRF.

Try to limit the time you spend on this to 2 hours.

Completion of all tasks is not mandatory. We do not want you to spend more time than required.

**It is totally OK not to finish the whole exercise.**

Still please pay attention to make sure that the parts delivered work. If they don't it's OK to add a comment to explain what you tried.

## Setup

1. Clone the repository
2. Create your own branch, can name it as your Github username

Feel free to use whatever process you use to develop code locally.

### Pre-requisites

The Python version used to write the code is `3.9.0`. A virtualenv was created and all packages used are in `requirements.txt`.

Once your virtualenv is set up, you can install all packages using:

```
pip install -r requirements.txt
```

Once at the repo's top-level run tests using `./manage.py test`. This should result in:

```
$ ./manage.py test                      
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....
----------------------------------------------------------------------
Ran 5 tests in 0.023s

OK
```

You could also do the below to run the Django server locally:

```
./manage.py migrate
./manage.py runserver
```

### Code formatting

Fully automated. Simply run this at project root:

```
isort .;black .
```

to have `isort` and `black` take care of the formatting.

### Current code

One app, called `articles` contains:

* `Article` model
* views:
  * `ListView` to be able to list/create articles
  * `DetailView` to be able to update/delete individual articles
* tests:
  * `APITestCase` to list/create article
  * `APITestCase` to update/delete individual articles

In short, the current app builds on DRF to provide an API to CRUD `Article`s.

## Task: Part 1. Enhance existing API

Leverage DRF tooling to

* Add ability to filter by articles `title` and `content`.
* Add ability to sort by article by `title` and `created_at`.

*Hints:*

* [https://www.django-rest-framework.org/api-guide/filtering/#filtering](https://www.django-rest-framework.org/api-guide/filtering/#filtering)
* [https://www.django-rest-framework.org/api-guide/filtering/#specifying-which-fields-may-be-ordered-against](https://www.django-rest-framework.org/api-guide/filtering/#specifying-which-fields-may-be-ordered-against)

## Task: Part 2. Add tests for Part 1

Use DRF `APITestCase` case to add tests that cover the filtering and ordering functionality added in `Part 1`.

*Hints:*

* Start by looking at how current tests are structured.
* Then add more test cases.

## Task: Part 3. Add tagging functionality

* Add `Tag` model, where a `Tag` can have a parent `Tag`.
  * We can have at maximum two levels in the hierarchy. 
    * Max one parent.
    * No multi-parent and/or tree structures.
  * Therefore `Tag` must have `name`, `slug`, and `parent` FK (nullable)
* Add API to be able to list/create `Tag`s.
* Add API to be able to add/remove Tag(s) to Article(s).
* Add API to list Articles by Tag.
  * Listing articles by `Tag` includes all articles related both to the tag itself *and* to any of its children.

**Tasks 4 and 5 are OPTIONAL. Only attempt once you have the above tasks working properly.**

## Task: Part 4. Add Tag update/delete functionality (optional)

* Only if you have spare time on your hands
* Add API to update/delete Tags
  * Prevent deletion of `Tag` when it has any Article(s) related to it
  * Prevent update of `Tag.slug` if it has any Article(s) related to it


## Task: Part 5. Add tests (optional)

* Only if you have spare time on your hands
* Use DRF `APITestCase` case to add tests for Parts 3 & 4 functionality.
