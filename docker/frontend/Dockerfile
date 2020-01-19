FROM node:latest as dev-stage

RUN mkdir /app
WORKDIR /app
COPY ./frontend/vueapp/package.json .
RUN npm install
COPY ./frontend/vueapp .
EXPOSE 80
CMD ["npm", "run", "serve"]

# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY ./frontend/vueapp/package.json .
RUN npm install
COPY ./frontend/vueapp .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY frontend/vueapp/nginx/default.conf /etc/nginx/conf.d/
COPY ssl/localhost.pem /etc/ssl/certs/server.pem
COPY ssl/localhost.key /etc/ssl/private/server.key

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]