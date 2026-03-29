FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm install && npm run build
EXPOSE 4000
CMD ["npm", "--workspace", "@siv/api", "run", "start"]
