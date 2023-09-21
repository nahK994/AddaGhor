FROM nginx:1.17.1-alpine
WORKDIR /Frontend
COPY . .
RUN npm install
RUN ng build
COPY /dist/Frontend /usr/share/nginx/html