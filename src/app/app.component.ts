import { Component, OnInit } from '@angular/core';
import { Servers } from './server';
import { StatusService } from './server-status.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  public servers: Servers = {};
  public responses: {[key: number]: string} = {
    200: "online"
  }

  constructor(private service: StatusService) {}

  async ngOnInit(): Promise<void> {
    this.servers = await this.service.getServerStatus();
  }
  keys(obj: object): string[] {
    return Object.keys(obj);
  }
  description(serverName: keyof Servers): string {
    const server = this.servers[serverName];

    const status = server["status"];
    if (status) return this.responses[status];

    const error = server["error"]
    if (!error) return "unknown"
    else return "offline";
  }
  error(serverName: keyof Servers): string | null {
    const error = this.servers[serverName]["error"];
    if (!error) return null;
    else return error;
  }
  logs(serverName: keyof Servers): string {
    const server = this.servers[serverName];
    const logs = server["logs"];
    
    if (!logs) return "No problems in the workspace";
    return logs;
  }
  overall(): string {
    return (Object.values(this.servers).every(
      s => s["status"] === 200) ? "All systems operational": "Something's gone wrong");
  }
}
