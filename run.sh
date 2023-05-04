echo "Loading database url..."
DB=`heroku config -a ukraine-image-bot`
export DATABASE_URL=$DB
python3 main.py