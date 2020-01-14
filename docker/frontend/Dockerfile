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

EXPOSE 80
#RUN sleep 100000000
CMD ["nginx", "-g", "daemon off;"]
#CMD ["nginx"]