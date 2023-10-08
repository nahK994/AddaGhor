import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PostService {

  readonly commandDomain = environment.commandDomain

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
    let response = await lastValueFrom(this.http.put<{id: number}>(this.commandDomain+URL_extention, payload, this.httpOptions));

    return response.id;
  }

  async createPost(postText: string) {
    let payload = {
      "text": postText
    };
    let response = await lastValueFrom(this.http.post<{id: number}>(this.commandDomain+'/posts', payload, this.httpOptions));

    return response.id;
  }
}
