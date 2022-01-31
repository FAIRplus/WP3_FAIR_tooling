#Base image
FROM node:lts-alpine

#Install serve package
RUN npm i -g serve

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# install project dependencies
RUN npm install
RUN npm install axios --save

# Copy the project files
COPY . .

# Expose a port
EXPOSE 8080

# Executables
CMD [ "npm", "run", "serve" ]