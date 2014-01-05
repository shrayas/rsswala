from app import app
from app import conf as config

# Run the app with params picked up from the config
app.run(
        debug=config.DEBUG,
        port=config.PORT,
        host=config.HOST
        )
