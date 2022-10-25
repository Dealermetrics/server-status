import { Injectable } from '@angular/core';
import axios from 'axios';
import { Servers } from './server';

@Injectable({
  providedIn: 'root'
})
export class StatusService {
  private url = "http://127.0.0.1:5001/api/servers"

  async getServerStatus(): Promise<Servers> {
    const response = await axios.get(this.url);
    return response.data;
  }
}