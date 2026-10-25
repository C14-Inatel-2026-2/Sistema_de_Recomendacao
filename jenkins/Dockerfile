FROM jenkins/jenkins:lts-jdk21

# O pipeline roda dentro deste proprio container (agent any),
# entao Python, Node e curl precisam estar instalados aqui.
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-venv curl ca-certificates gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*
USER jenkins

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
