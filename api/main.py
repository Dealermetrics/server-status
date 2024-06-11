import os
import re
import subprocess
import traceback
from typing import Any, Literal

import fastapi
import requests
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


@app.get("/status")
async def status() -> Literal[200]:
    return 200


def get_server_logs(server_domain: str) -> str:
    if os.name == "nt":
        with open("test/logs.txt", encoding="utf-8") as fp:
            return fp.read()

    process = subprocess.run(
        "systemctl status {}.service".format(server_domain.split(".")[0]),
        stdout=subprocess.PIPE,
        shell=True,
    )
    return process.stdout


@app.get("/servers")
def system_check():
    if os.name == "nt":
        dir = "test/sites-enabled"
    else:
        dir = "/etc/nginx/sites-enabled"

    servers: dict[str, dict[str, Any]] = {}
    for file in os.listdir(dir):
        if "status" in file: continue  # ignore the frontend status website
        if "default" in file: continue

        with open(os.path.join(dir, file)) as fp:
            content = fp.read()

        server_domains = re.findall(r"server_name\s+(.*?)[;]", content)
        if not server_domains:
            raise Exception()  # TODO: implement failing system

        server_domain: str = server_domains[0].strip()
        if "api" in server_domain:
            url = "api.dealermetrics.co.uk/status"  # avoid recursively calling itself
        else:
            url = server_domain

        try:
            response = requests.get(f"https://{url}/status")
            servers[server_domain] = {"status": response.status_code}
        except Exception as exc:
            logs = get_server_logs(server_domain)
            error = traceback.format_exception(exc)

            servers[server_domain] = {
                "error": error[-1],  # last error line
                "logs": logs,  # systemctl output
            }

    return servers


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=5001, host="0.0.0.0")
