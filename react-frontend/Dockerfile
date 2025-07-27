# Filename: react-frontend/Dockerfile

# --- Build Stage ---
# Use a Node.js image to build the React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Production Stage ---
# Use a lightweight Nginx server to host the static files
FROM nginx:stable-alpine
# Copy the built files from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html
# Tell Nginx to serve on port 80
EXPOSE 80
# Start Nginx
CMD ["nginx", "-g", "daemon off;"]