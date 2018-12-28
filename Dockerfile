FROM python:3.6-jessie

RUN apt-get update && apt-get install -y \
    vim \
    unzip

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
RUN bash ~/miniconda.sh -b -p ./miniconda
ENV PATH="/miniconda/bin:$PATH"

# add channels
RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge

RUN conda install -y STAR
RUN conda install -y samtools
RUN conda install -y tabix
RUN conda install -y picard
RUN conda install -y pytest

# install gatk
RUN wget https://github.com/broadinstitute/gatk/releases/download/4.0.12.0/gatk-4.0.12.0.zip
RUN unzip gatk-4.0.12.0.zip
ENV PATH="$PATH:/gatk-4.0.12.0/"

# make sure we have java 8. gatk needs 8
RUN conda install -y -c cyclus java-jdk

COPY . /gneiss
WORKDIR /gneiss

CMD /bin/bash
