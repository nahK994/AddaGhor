import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';

export interface CreateComment
{
  postId: number,
  userId: number,
  commentText: string
}

// export interface CreatePost
// {
//   userId: number,
//   postText: string
// }

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

  async updateComment(commentId: number, commentText: string) {
    let URL_extention = '/comment/'+commentId;
    let payload = {
      "text": commentText,

    }
    let response = await lastValueFrom(this.http.put<number>(this.baseUrl+URL_extention, payload, this.httpOptions));

    return response;
  }

  async updatePost(postId: number, postText: string) {
    let payload = {
      "text": postText
    }
    let URL_extention = '/post/'+postId;
    let response = await lastValueFrom(this.http.put<number>(this.baseUrl+URL_extention, payload, this.httpOptions));

    return response;
  }

  async createComment(postId: number, commentText: string) {
    let payload = {
      "postId": postId,
      "text": commentText
    }
    let response = await lastValueFrom(this.http.post<number>(this.baseUrl+'/comment', payload, this.httpOptions));

    return response;
  }

}
