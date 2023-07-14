import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';

export interface CreateComment
{
  postId: number,
  userId: number,
  commentText: string
}

export interface CreatePost
{
  userId: number,
  postText: string
}

@Injectable({
  providedIn: 'root'
})
export class PostCardService {

  baseUrl = ''

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  async reactPost(postId: number, reactType: 'like'|'smile'|'love') {
    let URL_extention = '/react/'+postId+'/'+reactType;
    let payload = {
      "reactType": reactType
    }
    let response = await lastValueFrom(this.http.put(this.baseUrl+URL_extention, payload, this.httpOptions));

    return response;
  }

  async updateComment(commentId: number, payload: CreateComment) {
    let URL_extention = '/comment/update/'+commentId;
    let response = await lastValueFrom(this.http.put<CreateComment>(this.baseUrl+URL_extention, payload, this.httpOptions));

    return response;
  }

  async updatePost(postId: number, payload: CreatePost) {
    let URL_extention = '/post/update/'+postId;
    let response = await lastValueFrom(this.http.put<CreatePost>(this.baseUrl+URL_extention, payload, this.httpOptions));

    return response;
  }

}
