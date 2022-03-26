import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CreateUser, LoginCredentialModel, User } from './user.interface';

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
    let response = await this.http.post<number>(this.baseUrl_Login+'/user/create', payload, this.httpOptions).toPromise();

    return response;
  }

  async updateUser(userId: number, payload: CreateUser) {
    let updateURL_extention = '/user/update/'+userId;
    let response = await this.http.put<CreateUser>(this.baseUrl_Login+updateURL_extention, payload, this.httpOptions).toPromise();

    return response;
  }

  async getUser(userId: number) {
    let updateURL_extention = '/users/'+userId;
    let response = await this.http.get<User>(this.baseUrl_Login+updateURL_extention, this.httpOptions).toPromise();

    return response;
  }

  async loginUser(loginInfo: LoginCredentialModel) {
    let updateURL_extention = '/login/'+loginInfo.email+'/'+loginInfo.password;
    let response = await this.http.get<number>(this.baseUrl_Login+updateURL_extention, this.httpOptions).toPromise();

    return response;
  }
}
