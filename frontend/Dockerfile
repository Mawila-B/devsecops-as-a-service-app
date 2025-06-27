FROM node:18-alpine

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* ./

RUN yarn install --frozen-lockfile || npm install

COPY . .

RUN yarn build || npm run build

EXPOSE 3000

CMD ["yarn", "start"]
