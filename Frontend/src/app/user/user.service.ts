import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import { environment } from 'src/environments/environment';

export interface CreateUser
{
  name: string,
  bio?: string,
  email: string,
  password: string,
  occupation: string,
  avatar: string
}

export interface User
{
  userId?: number,
  name: string,
  bio?: string,
  email: string,
  profilePicture?: string
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

  async createUser(payload: CreateUser) {
    let response = await lastValueFrom(this.http.post<number>(this.doamin+'/registration', payload, this.httpOptions));

    return response;
  }

  async updateUser(userId: number, payload: CreateUser) {
    let response = await lastValueFrom(this.http.put<CreateUser>(this.doamin+'/users/'+userId, payload, this.httpOptions));

    return response;
  }

  async getUser(userId: number) {
    let response = await lastValueFrom(this.http.get<User>(this.doamin+'/users/'+userId, this.httpOptions));

    return response;
  }
}
