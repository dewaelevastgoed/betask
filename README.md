# Task items Completed
## Description
- Created Base Model (Which consists commonly used fields) for Inheritance (Code Reusability)
- Structured the project similar to MVC Architecture
  - Every Model is defined in a single File - To increase readability
  - Same goes with Serializers
- Updated documentation for every feature updated with corresponding cURL's
- Created a Common module, which include base models and constants utilized in the project.
- Utilized base responses for reusability and faster development process
- Followed PEP8 standards with flake8 linter and black formatter
- Filtering, Ordering to existing Article API
- Tests for the updated Article API's
- Added Tag Creation/List/Updating/Deleting Functionality
- Tag articles


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

## Task: Part 1. Enhance existing API [DONE]

Leverage DRF tooling to

* Add ability to filter by articles `title` and `content`.
* Add ability to sort by article by `title` and `created_at`.

*Hints:*

* [https://www.django-rest-framework.org/api-guide/filtering/#filtering](https://www.django-rest-framework.org/api-guide/filtering/#filtering)
* [https://www.django-rest-framework.org/api-guide/filtering/#specifying-which-fields-may-be-ordered-against](https://www.django-rest-framework.org/api-guide/filtering/#specifying-which-fields-may-be-ordered-against)

### Endpoint to Filter and Order

```
curl --location --request GET 'http://127.0.0.1:8000/api/articles/?ordering=title'

curl --location --request GET 'http://127.0.0.1:8000/api/articles/?ordering=title&title=Dewaele'
```

## Task: Part 2. Add tests for Part 1 [DONE]

Use DRF `APITestCase` case to add tests that cover the filtering and ordering functionality added in `Part 1`.

*Hints:*

* Start by looking at how current tests are structured.
* Then add more test cases.

## Task: Part 3. Add tagging functionality [DONE]

* Add `Tag` model, where a `Tag` can have a parent `Tag`.
  * We can have at maximum two levels in the hierarchy. 
    * Max one parent.
    * No multi-parent and/or tree structures.
  * Therefore `Tag` must have `name`, `slug`, and `parent` FK (nullable)
* Add API to be able to list/create `Tag`s.
* Add API to be able to add/remove Tag(s) to Article(s).
* Add API to list Articles by Tag.
  * Listing articles by `Tag` includes all articles related both to the tag itself *and* to any of its children.

### API to create or get list of Tags

### List Articles by Tag name
```
curl --location --request GET 'http://127.0.0.1:8000/api/articles/?search=lead'
```

### Creating a Tag
```
curl --location --request POST 'http://127.0.0.1:8000/api/tags/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Jr Lead 2",
    "slug": "jr-lead-slug-2",
    "parent":null
}'
```
### List of All tags
```
curl --location --request GET 'http://127.0.0.1:8000/api/tags/'
```

### Add or Removing Tags

```
curl --location --request PUT 'http://127.0.0.1:8000/api/articles/5/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tags": [
        1
    ],
    "title": "DewaeleGroup",
    "slug": "real-estate-project-discussion",
    "content": "Dewaele Group is working on new projects to improve real estate experience"
}'
```

**Tasks 4 and 5 are OPTIONAL. Only attempt once you have the above tasks working properly.**

## Task: Part 4. Add Tag update/delete functionality (optional) [DONE]

* Only if you have spare time on your hands
* Add API to update/delete Tags
  * Prevent deletion of `Tag` when it has any Article(s) related to it
  * Prevent update of `Tag.slug` if it has any Article(s) related to it

### Tag Update View
```
curl --location --request PUT 'http://127.0.0.1:8000/api/tags/2/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Sr Lead",
    "slug": "senior-lead"
}'
```

### Tag Delete View
```
curl --location --request DELETE 'http://127.0.0.1:8000/api/tags/2/'
```

## Task: Part 5. Add tests (optional)

* Only if you have spare time on your hands
* Use DRF `APITestCase` case to add tests for Parts 3 & 4 functionality.
