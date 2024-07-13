FROM python:3.12 AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12

WORKDIR /backend

COPY --from=requirements-stage /tmp/requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ./app /backend/app

EXPOSE 8000

#CMD ["uvicorn", "--factory", "app.main:create_app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
CMD ["fastapi", "run", "app/main", "--root-path", "/api"]