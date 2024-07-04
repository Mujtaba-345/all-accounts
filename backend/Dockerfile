FROM python:3.11

#ARG RELEASE_VERSION=${RELEASE_VERSION:-0.0.0}
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#ENV RELEASE_VERSION $RELEASE_VERSION

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install poetry

RUN apt-get update \
    && apt-get install -y libpq-dev gcc python3-dev musl-dev libjpeg-dev zlib1g-dev \
       git supervisor ffmpeg curl libffi-dev nano

# Copy the poetry files and install dependencies
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000



# Copy entrypoint script and make it executable
# COPY ./backend/entrypoint.sh /usr/src/app/backend/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=all_accounts.settings

# Run the entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
