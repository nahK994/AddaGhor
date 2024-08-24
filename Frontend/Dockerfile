FROM node:18.19 AS build
WORKDIR /Frontend
COPY . .

RUN npm install

RUN npm install -g @angular/cli
RUN ng build --configuration=development

CMD ["ng", "serve", "--host", "0.0.0.0"]