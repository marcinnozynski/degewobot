build-image:
	docker build --tag europe-west3-docker.pkg.dev/degewobot/images/degewobot:latest .

push-image:
	docker push europe-west3-docker.pkg.dev/degewobot/images/degewobot:latest

build-push-image: build-image push-image
