ARG PYTHON_VERSION=3.13-alpine

FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY pyproject.toml uv.lock /code/
RUN uv sync
COPY . /code

EXPOSE 8000

CMD ["uv", "run", "gunicorn","--bind",":8000","--workers","2","formi.wsgi"]
