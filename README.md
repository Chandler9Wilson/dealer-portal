# Dealer Portal

---

## About

* Project overview
  * This project is designed to keep track of customers, locations, and devices of a company that sells sensor packages for predictive maintence.
  * The above data can be thought of as a hierarchical structure as follows

```bash
├── Customer
│   ├── Facility
│       ├── Device
```

## Getting started

* First time setup
  1. Run `./server_managment/setup_script.py` respond yes when prompted if this is your first time.
  2. `$ source env/bin/activate`
  3. `$ pip install -r requirements.txt`

* Navigating the project
  * The majority of the server codebase is split into `flask blueprints` within the `portal_server` package
  * Most of the frontend code is found within `.vue` files under `./portal_server/directory/home_static/src/components/`

## Viewing the Documentation (Not written currently)

1. Activate your env with `source env/bin/activate`
2. `cd docs`
3. `make html`
4. `python -m http.server`
5. Navigate to build/html

## TODO

* Frontend Menu layout
* Implement flask principle for finer grained user permissions
* update variable names to follow [this](http://flask.pocoo.org/docs/0.12/styleguide/#naming-conventions)
* remove debug prints
* remove all references to `catalog` changed name to `dealer_portal`
* write documentation on db scripts
* Add better server side validation

## Development

* Style
  * JS = [StandardJS](https://standardjs.com/)
  * Python = [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Frontend tooling
  * webpack can be run with `$ npm run` find the commands in ./static/package.json

## Debugging

* Tools
  * with pudb (recommended)
    * insert where you want a breakpoint `from pudb import set_trace; set_trace()`
  * with pdb
    * insert `import pdb; pdb.set_trace()`
* Tips for api and auth
  * Make sure you are sending credentials
  * Make sure to disable cache if using a browser during development
  * Make sure you are building using webpack if working on anything in directory static



## TO READ

* [things which arent magic flask](https://ains.co/blog/things-which-arent-magic-flask-part-1.html)
* [Best Practices for function arguments](http://www.informit.com/articles/article.aspx?p=2314818)
* [decorators documentation](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
* [how does the property decorator work?](https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work)
* [how to make a chain of function decorators?](https://stackoverflow.com/a/1594484/6879253)

## Resources

* Sphinx [tutorial](https://media.readthedocs.org/pdf/brandons-sphinx-tutorial/latest/brandons-sphinx-tutorial.pdf) extremely helpful
* flask [Blueprints](https://books.google.com/books/about/Flask_Blueprints.html?id=SfSoCwAAQBAJ&printsec=frontcover&source=kp_read_button#v=onepage&q&f=true)
* python subprocess [explanation](http://www.codecalamity.com/run-subprocess-run/)
* [REST api](http://www.restapitutorial.com)
* [python import confustion](http://effbot.org/zone/import-confusion.htm)