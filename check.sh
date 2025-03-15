#!/bin/sh

echo "Running black..."
poetry run black .
echo

echo "Running mypy..."
poetry run mypy .
echo

echo "Running isort..."
poetry run isort .
