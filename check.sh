#!/bin/sh

echo "Running ruff..."
uv tool run ruff check --fix
echo

echo "Running mypy..."
uv run mypy .
echo
