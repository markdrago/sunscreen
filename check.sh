#!/bin/sh

echo "Running black..."
uv tool run black .
echo

echo "Running mypy..."
uv run mypy .
echo

echo "Running isort..."
uv tool run isort .
