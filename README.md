# RUMAD Monitor

A framework of commands and helper classes to scrape RUMAD 😏. Contains collection of controllers and SMTP tooling to send notifications via email about availability of sections (secciones) of classes and semester.

**Demo in action:** [`jobs/matricula.py`](./jobs/matricula.py). 
A basic script with example of how to fetch class information and send notification via email. 

To run the **demo**, in the `root` directory of the project execute the cmd:

```
PYTHONPATH=. py ./jobs/matricula.py
```

## Supported Version(s)

- Developed and tested in **Python 3.6+**

## Usage

### Recomended usage

Use your system cronjobs to schedule the running of your custom `jobs`. Jobs can be created and saved in [`./jobs/`](./jobs).

### Install and Development

#### Python Environment 

Use https://docs.python.org/3/library/venv.html for ease of python management.

After selecting your python environment run:

```
python -m pip -r requirements.txt
``` 

to install the required dependencies.

#### Dotenv

Copy [`.env.example`](./.env.example) and name it `.env`, then fill the environment variables with the required values.


## Tests/Testing

### Unittest

In the `root` directory run:

```
py -m unittest
```

### Integration test

To test the SMTP (email) feature against a real server change the `INTEGRATION_TESTS` flag in the `.env` to `true`.

*Beware, the aforementioned will execute the SMTP drivers and try to establish a connection with the **SMTP server host** specified in the `.env` file.

### Adding more test

The tests are implemented with https://docs.python.org/3/library/unittest.html.

**NOTE:** You are welcome to add more tests as needed.