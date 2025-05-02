# Homework 4
There's two example docker image: mitmproxy, nextjs

## Nextjs Example App
```
cd hw4/nextjs
docker build -t nextjs-example-app .
docker run -p 3000:3000 nextjs-example-app
```


## Mitmproxy Example App
```
cd hw4/mitmproxy
docker build -t mitmproxy-example .
docker run --rm -it --net=host --cap-add=NET_ADMIN mitmproxy-example
```