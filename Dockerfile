FROM python:3.11.9-bullseye AS base
RUN pip install pdm

FROM oven/bun:1 as style_builder
WORKDIR /app
COPY . .
RUN bun install
RUN bun run build

FROM base AS builder
WORKDIR /app
COPY . .
COPY --from=style_builder /app/src/todo/static/tailwind.css /app/src/todo/static/tailwind.css
RUN pdm install
RUN pdm run src/manage.py collectstatic --noinput

EXPOSE 8000
CMD ["pdm", "run", "src/manage.py", "runserver", "0.0.0.0:8000"]

