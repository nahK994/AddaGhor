FROM node:14.21 AS build
WORKDIR /Frontend
COPY . .

# RUN npm install @angular/common@^9.1.11
RUN npm install
# RUN npm audit fix
RUN npm install -g @angular/cli
RUN ng build --configuration=development

FROM nginx:1.17.1-alpine
COPY --from=build /Frontend/dist/Frontend /usr/share/nginx/html