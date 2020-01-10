FROM node:latest

RUN mkdir /app
WORKDIR /app
COPY ./frontend/vueapp/package.json .
RUN npm install
COPY ./frontend/vueapp .
EXPOSE 5000
CMD ["npm", "run", "serve"]