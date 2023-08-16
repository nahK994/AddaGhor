import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';

export interface CreateUser
{
  userName: string,
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

  baseUrl_Login: string = 'http://localhost:8000';
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  async createUser(payload: CreateUser) {
    let response = await lastValueFrom(this.http.post<number>(this.baseUrl_Login+'/registration', payload, this.httpOptions));

    return response;
  }

  async updateUser(userId: number, payload: CreateUser) {
    let response = await lastValueFrom(this.http.put<CreateUser>(this.baseUrl_Login+'/users/'+userId, payload, this.httpOptions));

    return response;
  }

  async getUser(userId: number) {
    let response = await lastValueFrom(this.http.get<User>(this.baseUrl_Login+'/users/'+userId, this.httpOptions));

    return response;
  }
}
