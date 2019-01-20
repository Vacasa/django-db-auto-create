# Django DB Auto Create

## What is this?

Django doesn't create databases for you automatically. You have to do this yourself manually.

This is a simple package that creates your database for you automatically, if necessary, when you run `migrate` for the first time.

**Important: This package only supports PostgreSQL at the moment!**

## Quickstart

- add `django_db_auto_create` to your project's INSTALLED_APPS
- add `"AUTO_CREATE": True` to your database settings