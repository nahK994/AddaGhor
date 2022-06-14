# FROM node:14.19.3-alpine as build-step
# WORKDIR /Frontend
# COPY ./ ./
# RUN npm install
# RUN npm audit fix
# RUN npm run build

# FROM nginx:1.17.1-alpine
# COPY --from=build-step /dist/Frontend /usr/share/nginx/html

FROM nginx:1.17.1-alpine
COPY /dist/Frontend /usr/share/nginx/html