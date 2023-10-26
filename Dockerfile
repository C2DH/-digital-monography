FROM python:3.11-slim

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


# Install dependencies for transforming .html to .pdf
RUN apt-get update && apt-get install -y \
    gconf-service \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgcc1 \
    libgconf-2-4 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator1 \
    libnss3 \
    lsb-release \
    xdg-utils \
    wget

# Give the user permissions to write to /data directory.
COPY /data /data
RUN chown -R app_user:app_user /data
RUN chmod +rwx------ /data

# Give the user permissions to write to /logs directory.
COPY /logs /logs
RUN chown -R app_user:app_user /logs
RUN chmod +rwx------ /logs

# Change the user to the previously created __app_user__.
USER app_user

# Copy application source code from Dockerfile dir in the host 
# to the `/home/app_user` dir in the container.
COPY . .

# Set bash as default command,
# which will be invoked when docker container runs.
CMD ["bash"]
