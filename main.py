import os
import subprocess

from dotenv import load_dotenv

load_dotenv()


def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "8082")
    os.environ["PYTHONPATH"] = ":".join(os.getenv("PYTHONPATH", "").split(":")) + ":."
    subprocess.run(
        [
            "uv",
            "run",
            "litellm",
            "--config",
            "config.yaml",
            "--host",
            host,
            "--port",
            port,
        ]
    )


if __name__ == "__main__":
    main()
