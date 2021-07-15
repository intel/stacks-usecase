#Copyright (c) 2021, Intel Corporation.
#SPDX-License-Identifier: BSD-3-Clause


# build environment

FROM node:16.2.0-alpine as build

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY /src/ui_controller/package.json ./
COPY /src/ui_controller/package-lock.json ./
RUN npm install -g npm@7.14.0 && \
    npm config set registry http://registry.npmjs.org/ && \
    npm ci && \
    npm install react-scripts -g
COPY ./src/ui_controller ./
RUN npm run build


# production environment

FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
# new
COPY /src/ui_controller/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
