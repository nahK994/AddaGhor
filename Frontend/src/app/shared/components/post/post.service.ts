import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PostService {

  baseUrl_Post: string = 'http://localhost:8001';

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  async updatePost(postId: number, postText: string) {
    let payload = {
      "text": postText
    }
    let URL_extention = '/posts/'+postId;
    let response = await lastValueFrom(this.http.put<number>(this.baseUrl_Post+URL_extention, payload, this.httpOptions));

    return response;
  }

  async createPost(postText: string) {
    let payload = {
      "text": postText
    };
    let response = await lastValueFrom(this.http.post<number>(this.baseUrl_Post+'/posts', payload, this.httpOptions));

    return response;
  }
}
