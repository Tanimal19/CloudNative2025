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

# Workflow
![push flow](./push-flow.png)

1. specify the version in Dockerfile
2. some changes been push to repo
3. trigger Actions if the change is make under `hw4/**`
4. Actions extract version from Dockerfile and combine it with the project folder name
5. Actions build and push the image to docker hub