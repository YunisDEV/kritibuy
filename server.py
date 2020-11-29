from src import app
import config
if __name__ == "__main__":
    app.run(debug=config.DEBUG,port=config.PORT,host=config.HOST)
