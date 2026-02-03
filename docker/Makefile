all:

push: # build
	docker tag testok dtorrance/m2jk
	docker push dtorrance/m2jk

run: # build
	docker run -p 8890:8890 testok

build:
	cp ../demo/test.ipynb .
	cp ../demo/demo.ipynb .
	docker build --tag testok . --no-cache
