FROM mambaorg/micromamba:bookworm-slim

#micromamba defaults to a non-root user
USER root
RUN useradd --create-home --shell /bin/bash newuser

WORKDIR /home/newuser
USER newuser

COPY requirements/docker.yml .
# Create the environment:
RUN micromamba install --yes --name base -f docker.yml
RUN micromamba clean --all --yes

# Activate the environment, 
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# copy gimbleprep code
COPY . .

ENTRYPOINT ["/opt/conda/bin/python3", "gimbleprep.py"]