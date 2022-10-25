import { Injectable } from '@angular/core';
import axios from 'axios';
import { Servers } from './server';

@Injectable({
  providedIn: 'root'
})
export class StatusService {
  private url = "https://status.caedenph.com/api/servers"

  async getServerStatus(): Promise<Servers> {
    const response = await axios.get(this.url);
    return response.data;
  }
}