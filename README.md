# Dealer Portal

## This readme is for the Back-end e.g. Flask and DB management for Front-end work see the readme in ./static

## TODO

* Update fake_customer_data devices to have all required fields currently missing hardware_id
* Frontend Menu layout
* Display fake data
* Implement flask principle for finer grained user permissions
* update variable names to follow [this](http://flask.pocoo.org/docs/0.12/styleguide/#naming-conventions)
* remove debug prints
* remove all references to `catalog` changed name to `dealer_portal`
* write documentation on db scripts
* Make `import_fake_data.py` more robust e.g. able to add a device without customer or facility

## Development

* Style
  * JS = [StandardJS](https://standardjs.com/)
  * Python = [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Frontend tooling
  * webpack can be run with `$ npm run` find the commands in ./static/package.json

## Debugging

* with pdb
  * insert `import pdb`
  * && `pdb.set_trace()`

## Resources

* python subprocess [explanation](http://www.codecalamity.com/run-subprocess-run/)