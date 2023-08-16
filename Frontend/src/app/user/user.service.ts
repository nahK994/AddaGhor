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
    let response = await lastValueFrom(this.http.post<number>(this.baseUrl_Login+'/users/create', payload, this.httpOptions));

    return response;
  }

  async updateUser(userId: number, payload: CreateUser) {
    let updateURL_extention = '/users/update/'+userId;
    let response = await this.http.put<CreateUser>(this.baseUrl_Login+updateURL_extention, payload, this.httpOptions).toPromise();

    return response;
  }

  async getUser(userId: number) {
    let updateURL_extention = '/users/'+userId;
    let response = await this.http.get<User>(this.baseUrl_Login+updateURL_extention, this.httpOptions).toPromise();

    return response;
  }
}
