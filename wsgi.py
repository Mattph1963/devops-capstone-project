from service import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Get the port from the environment variable, default to 8080 if not set
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
