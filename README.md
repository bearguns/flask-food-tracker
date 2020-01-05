# flask-food-tracker
This is a simple Flask example application built following [The Ultimate Flask Course](https://www.udemy.com/course/the-ultimate-flask-course/) on Udemy.

## Getting Started

### Prerequisites
- Python 3
- pip3 and pipenv to install dependencies and create virtualenv
- sqlite3

### Setting up the local DB
- Create a new database i.e. `$ sqlite3 food-tracker.db`.
- Create the neccessary tables using the `.sql` file in the repo.
`$ sqlite3 /name/of/local/db < /path/to/repo/food-tracker.sql`

### Running the app
- `cd` into the app directory, and run `pipenv install` to install dependencies and create the virtual environment.
- Start the virtual shell with `pipenv shell`
- Start the Flask server with `flask run`.

Hope this code is helpful to you as you learn Flask and Python3!
