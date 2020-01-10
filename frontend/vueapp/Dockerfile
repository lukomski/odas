FROM node:latest

RUN mkdir /app
WORKDIR /app

COPY ./package.json .

#RUN npm install -g @vue/cli
#RUN npm install -g @vue/cli-service-global
#RUN npm install --save vue-router
#RUN npm install vue bootstrap-vue bootstrap
#RUN npm i axios --global


RUN npm install
COPY ./ .
RUN sleep 100000
EXPOSE 5000
CMD ["npm", "run", "serve"]
