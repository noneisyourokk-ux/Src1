# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client
import importlib
import os
import sys
from flask import Flask
from threading import Thread

# ======================================================
# 🚀 Render Flask Web Server (To keep bot alive)
# ======================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ======================================================
# 🤖 Main Bot Logic
# ======================================================
async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()  

async def main():
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)  

if __name__ == "__main__":
    # Flask ko alag thread me start kar rahe hain taaki Render port binding verify kar sake
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    print("🌐 Web server started on port 5000...")

    loop = asyncio.get_event_loop()
    print("Starting clients ...")
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        sys.exit(1)
    finally:
        try:
            loop.close()
        except Exception:
            pass
