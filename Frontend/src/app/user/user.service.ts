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

  readonly doamin = environment.domain;
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  async createUser(payload: User) {
    payload.profilePicture = ""
    let response = await lastValueFrom(this.http.post<number>(this.doamin+'/registration', payload, this.httpOptions));

    return response;
  }

  async updateUser(userId: number, payload: User) {
    payload.profilePicture = ""
    let response = await lastValueFrom(this.http.put<User>(this.doamin+'/users/'+userId, payload, this.httpOptions));

    return response;
  }

  async getUser(userId: number) {
    let response = await lastValueFrom(this.http.get<User>(this.doamin+'/users/'+userId, this.httpOptions));

    return response;
  }
}
