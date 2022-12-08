FROM --platform=linux/amd64 golang:1.19.3-alpine3.15

WORKDIR /go
COPY gateway-api .
COPY kubeconfig .
EXPOSE 8080
ENTRYPOINT ["./gateway-api"]

