#!/usr/bin/env bash

set -e

alembic upgrade head
exec python -m aiogram_template