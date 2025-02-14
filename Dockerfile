FROM axiom/docker-luigi:2.8.13-alpine AS luigi
# This build stage only exists to grab files

FROM mambaorg/micromamba:1.2.0 AS micromamba
COPY --from=luigi /bin/run /usr/local/bin/luigid
USER root

# `libgl1-mesa-glx` is required for pyqgis
# `git` is required for analyzing the current version
# `make` is required for building sphinx docs
# `texlive-latex-extra` is required for pdf doc builds
RUN apt-get update && apt-get install -y \
  git \
  make \
  libgl1-mesa-glx \
  texlive-latex-extra

# Create environments
RUN micromamba install -y -c conda-forge -n base conda mamba~=1.2.0

COPY --chown=mambauser:mambauser environment-lock.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml

COPY --chown=mambauser:mambauser environment.cmd.yml /tmp/environment.cmd.yml
RUN micromamba create -y -f /tmp/environment.cmd.yml

# Cleanup
RUN micromamba clean --all --yes

WORKDIR /luigi

# Everything is installed to the base conda environment, but the docker image
# doesn't activate the env automatically, which is how the PYTHONPATH normally
# gets populated. Additionally, /luigi/tasks is where we expect python code to
# be mounted.
ENV PYTHONPATH /luigi/tasks/qgreenland:/opt/conda/share/qgis/python/plugins:/opt/conda/share/qgis/python
ENV PATH /opt/conda/bin:$PATH

CMD ["/usr/local/bin/luigid"]
