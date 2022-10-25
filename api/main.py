import os
import re
import traceback
import subprocess
import requests

import fastapi

app = fastapi.FastAPI()


@app.get("/api/systems")
def system_check():
    if os.name == "nt": dir = "test/sites-enabled"
    else: dir = "/etc/nginx/sites-enabled"

    systems = {}
    for file in os.listdir(dir):
        with open(os.path.join(dir, file)) as fp:
            content = fp.read()

        server_domains = re.findall("server_name\s+(.*?)[;]", content)
        if not server_domains: 
            continue  # TODO: implement failing system

        server_domain: str = server_domains[0].strip()
        try:
            response = requests.get(f"https://{server_domain}")
            systems[server_domain] = {
                "status": response.status_code
            }
        except Exception:
            process = subprocess.run(
                "systemctl status {}.service".format(
                    server_domain.split(".")[0]
                ),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            systems[server_domain] = {
                "error": traceback.format_exc(),
                "logs": {
                    "stdout": process.stdout,
                    "stderr": process.stderr
                }
            }

    return systems

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=5001, host="0.0.0.0")