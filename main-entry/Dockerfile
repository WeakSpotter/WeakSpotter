FROM node:14
WORKDIR /usr/src/app
COPY app/ . 
RUN npm install express axios
EXPOSE 80
CMD ["node", "server.js"]
