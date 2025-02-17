FROM python:3.12-slim

RUN python3 -m venv /opt/venv

# Install dependencies:
COPY ../requirements/prod.in .

# Copy in files we need
COPY pyproject.toml .
COPY src/myapp/web/app.py app-server/
COPY src/myapp/web/__init__.py app-server/
COPY dist/fast_app-0.0.0-py3-none-any.whl .
COPY ./conf/test.toml /conf/conf.toml

# Install requirements
RUN . /opt/venv/bin/activate && pip install -r prod.in
RUN . /opt/venv/bin/activate && pip install fast_app-0.0.0-py3-none-any.whl 

WORKDIR /opt/venv/

# Expose the port that FastAPI will run on
EXPOSE 8000

CMD ["bin/uvicorn", "--app-dir", "/app-server/", "app:app", "--host", "0.0.0.0", "--port", "8000"]
