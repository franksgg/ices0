FROM debian:latest
LABEL authors="frank"
RUN apt-get update
RUN apt-get update
RUN apt-get install -y git build-essential cmake libmp3lame-dev libflac-dev libxml2-dev libshout-dev libvorbis-dev libogg-dev libfaad-dev libpython3-dev libperl-dev
RUN git clone https://github.com/franksgg/ices0.git
WORKDIR /ices0
RUN mkdir "build"
#RUN cmake --help
RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
      -DWITH_XML=ON -DWITH_PYTHON=ON -DWITH_PERL=ON -DWITH_LAME=ON \
      -DWITH_VORBIS=ON -DWITH_FAAD=ON -DWITH_FLAC=ON
RUN cmake --build build
RUN cmake --install build
ENTRYPOINT ["ices", "-c /etc/ices/ices.conf"]