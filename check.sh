#!/bin/sh

echo "Running mypy..."
poetry run mypy .
echo

echo "Running isort..."
poetry run isort .
echo

echo "Running black..."
poetry run black .

