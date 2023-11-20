FROM python:3.11
# FROM python:3.11-slim

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


# Install dependencies for transforming .md to .ipynb
RUN wget https://github.com/jgm/pandoc/releases/download/3.1.9/pandoc-3.1.9-1-amd64.deb &&\
    dpkg -i pandoc-3.1.9-1-amd64.deb

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

# Give pytest permissions to cache tests results.
COPY /tests /tests
RUN mkdir /tests/.pytest_cache
RUN chown -R app_user:app_user /tests/.pytest_cache
RUN chmod +rwx------ /tests/.pytest_cache
# Give pytest permissions to cache tests auxiliaries.
RUN mkdir /.pytest_cache
RUN chown -R app_user:app_user /.pytest_cache
RUN chmod +rwx------ /.pytest_cache

# Add PYTHONPATH to change the search path for libraries.
# The search path should be the same for all of the scripts (inlc. tests).
ENV PYTHONPATH "${PYTHONPATH}:/"

# Change the user to the previously created __app_user__.
USER app_user

# # Download nvm and load it to the environment variables.
# # Install mystmd and it's dependencies.
# # Probably should be moved after 'CMD ["bash"]'...
# RUN ["/bin/bash", \
#     "-c", \
#     "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash && \
#     source ~/.nvm/nvm.sh && \
#     nvm install 20.9.0 && \
#     npm install -g npm && \
#     npm install -g mystmd@1.1.26"]

COPY . .

# Set bash as default command,
# which will be invoked when docker container runs.
CMD ["bash"]
