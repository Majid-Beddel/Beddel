# Use Node.js LTS base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and lock file
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the default Next.js dev port
EXPOSE 3000

# Start the dev server (or use `next start` if pre-built)
CMD ["npm", "run", "dev"]
