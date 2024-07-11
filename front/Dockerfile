FROM node:lts-alpine as setup-stage

WORKDIR /front

ENV PATH /front/node_modules/.bin:$PATH

COPY package*.json /front/

RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine as prod-stage

COPY --from=setup-stage /front/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]