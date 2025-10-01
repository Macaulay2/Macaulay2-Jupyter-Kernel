FROM jupyter/base-notebook

# install m2jk and copy examples
RUN python3 -m pip install macaulay2-jupyter-kernel
RUN python3 -m m2_kernel.install
COPY test.ipynb /test/
COPY demo.ipynb /test/

# install M2
USER root
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:macaulay2/macaulay2
RUN apt-get update && apt-get install -y macaulay2

# run jupyter notebook
USER jovyan
WORKDIR /test
ENTRYPOINT ["jupyter", "notebook", "--port", "8890", "--no-browser"]
EXPOSE 8890