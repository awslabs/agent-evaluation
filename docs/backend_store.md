# Backend Store

The backend store is a relational database that contains information about your runs, tests, and test results.

## Configure a backend store

The default backend store is a local SQLite database, which is created and stored in the current working directory.

To use a different database, you can specify the database URL with one of the following methods:

1. Use the `--backend-store-url` CLI option.
2. Set the `AGENTEVAL_BACKEND_STORE_URL` environment variable.

!!! note
    Agent Evaluation uses [SQLAlchemy](https://www.sqlalchemy.org/) to interface with the backend store database. Please make sure the database URL follows the format outlined in the [documentation](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls).


## Using the backend store

The CLI provides several convenient commands to fetch data from the backend store. Please refer to the [CLI documentation](cli.md#agenteval-store) for more details.

## Upgrading the backend store

If the schema for the backend store is outdated, you can upgrade it to the latest supported version using `agenteval store upgrade`.

!!! note
    Schema upgrades can be slow and not guaranteed to be transactional. Always take a backup of your database before executing the upgrade.
