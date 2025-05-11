FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Expose Angular dev server port
EXPOSE 4200

# Run Angular dev server
CMD ["npm", "run", "start"]