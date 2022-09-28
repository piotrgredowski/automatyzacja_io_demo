# automatyzacja_io_demo

---

**Documentation**: [https://piotrgredowski.github.io/automatyzacja_io_demo](https://piotrgredowski.github.io/automatyzacja_io_demo)

**Source Code**: [https://github.com/piotrgredowski/automatyzacja_io_demo](https://github.com/piotrgredowski/automatyzacja_io_demo)


---

This is just a demo service for automatyzacja.io conference.

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/) 1.2.1
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
poetry run pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```
