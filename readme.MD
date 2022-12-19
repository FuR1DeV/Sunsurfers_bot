В файле docker-compose.yml  
POSTGRES_USER: "" - Имя пользователя  
POSTGRES_PASSWORD: "" - Пароль  
  
Создаём файл .env, куда вписываем хост (HOST), имя юзера бд(POSTGRESQL_USER), пароль от бд (POSTGRESQL_PASSWORD) и название бд (DATABASE) токен бота (BOT_TOKEN) а так же ADMIN_ID в таком виде id, сейчас вписан айди разработчика этого бота  
  
HOST="db"  
POSTGRESQL_USER=""  
POSTGRESQL_PASSWORD=""  
DATABASE="sunsurfers_tg_bot"  
BOT_TOKEN=""  
ADMIN_ID="351490585,"  
  
- Запуск основного бота, производится путём запуска main.py  
- Команда /start для пользователей.  
- Команда /admin для админов.  
  
