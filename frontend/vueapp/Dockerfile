FROM node:latest

RUN npm install -g @vue/cli
RUN npm install -g @vue/cli-service-global
RUN npm install --save vue-router
RUN npm install vue bootstrap-vue bootstrap
RUN npm i axios --global 

RUN mkdir /app
WORKDIR /app
COPY ./ .
RUN npm install
EXPOSE 5000
CMD ["npm", "run", "serve"]
