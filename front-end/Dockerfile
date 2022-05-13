FROM node:lts as build-stage
RUN export NODE_OPTIONS=--max_old_space_size=1536
WORKDIR /app
COPY package*.json ./
RUN npm cache clean -f
RUN rm -rf node_modules package-lock.json && npm install --legacy-peer-deps
COPY ./ .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf