# Dealer Portal

## This readme is for the Back-end e.g. Flask and DB management for Front-end work see the readme in ./static

---

## Getting started

1. Run `./server_managment/setup_script.py` respond `y` when prompted if this is your first time.

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

* with pudb (recommended)
  * insert where you want a breakpoint `from pudb import set_trace; set_trace()`
* with pdb
  * insert `import pdb`
  * && `pdb.set_trace()`

## TO READ

* [things which arent magic flask](https://ains.co/blog/things-which-arent-magic-flask-part-1.html)
* [decorators documentation](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
* [how does the property decorator work?](https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work)
* [how to make a chain of function decorators?](https://stackoverflow.com/a/1594484/6879253)

## Resources

* python subprocess [explanation](http://www.codecalamity.com/run-subprocess-run/)
* [REST api](http://www.restapitutorial.com)
* [python import confustion](http://effbot.org/zone/import-confusion.htm)