FROM python:3.10-slim

# Due to security reasons, 
# it’s a good practice to run containers as a non-root user.
# Option `--create-home` will create user’s home directory.
# `--shell bin/bash` make sure bash is the default shell.
RUN useradd --create-home --shell /bin/bash app_user

# Copy the requirements.txt file
COPY /requirements /requirements

# Install all required packages.
# Disable the cash using `--no-cache-dir` option to lower image size.
RUN pip install -r requirements/dev.txt
# RUN pip install --no-cache-dir -r requirements/prod.txt

# Give the user permissions to write to /data directory.
COPY /data /data
RUN chown -R app_user:app_user /data
RUN chmod 755 /data

# Change the user to the previously created __app_user__.
USER app_user

# Copy application source code from Dockerfile dir in the host 
# to the `/home/app_user` dir in the container.
COPY . .

# Set bash as default command,
# which will be invoked when docker container runs.
CMD ["bash"]
