FROM python:3.6-jessie

RUN apt-get update
RUN yes | apt-get install vim

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
RUN bash ~/miniconda.sh -b -p ./miniconda
ENV PATH="/miniconda/bin:$PATH"

# add channels
RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge

RUN conda install -y STAR
RUN conda install -y samtools
RUN conda install -y pytest

COPY . /gneiss
WORKDIR /gneiss

CMD /bin/bash
