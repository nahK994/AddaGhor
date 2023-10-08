import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import { environment } from 'src/environments/environment';

export interface User
{
  userId?: number,
  name: string,
  bio?: string,
  email: string,
  profilePicture?: string,
  password?: string
}

@Injectable({
  providedIn: 'root'
})
export class UserService {

  readonly queryDoamin = environment.queryDomain;
  readonly commandDoamin = environment.commandDomain;

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  async createUser(payload: User) {
    delete payload.profilePicture
    let response = await lastValueFrom(this.http.post<number>(this.commandDoamin+'/registration', payload, this.httpOptions));

    return response;
  }

  async updateUser(userId: number, payload: User) {
    delete payload.profilePicture
    let response = await lastValueFrom(this.http.put<User>(this.commandDoamin+'/users/'+userId, payload, this.httpOptions));

    return response;
  }

  async getUser(userId: number) {
    let response = await lastValueFrom(this.http.get<User>(this.queryDoamin+'/users/'+userId, this.httpOptions));

    return response;
  }
}
