import { Injectable } from '@angular/core';
import axios from 'axios';
import { Servers } from './server';

@Injectable({
  providedIn: 'root'
})
export class StatusService {
  private url = "https://api.dealermetrics.co.uk/servers"
  // private url = "http://127.0.0.1:5001/servers"

  async getServerStatus(): Promise<Servers> {
    const response = await axios.get(this.url);
    return response.data;
  }
}