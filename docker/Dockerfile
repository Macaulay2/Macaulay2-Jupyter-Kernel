FROM jupyter/base-notebook

# install M2
USER root
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:macaulay2/macaulay2
RUN apt-get install -y macaulay2 git
RUN mkdir -p /test && chown -R jovyan:users /test

# install m2jk and copy examples
USER jovyan
RUN python3 -m pip install git+https://github.com/Macaulay2/Macaulay2-Jupyter-Kernel
RUN python3 -m m2_kernel install --user
COPY test.ipynb /test/
COPY demo.ipynb /test/

# run jupyter notebook
WORKDIR /test
ENTRYPOINT ["jupyter", "lab", "--port", "8890", "--no-browser"]
EXPOSE 8890