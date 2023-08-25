import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import { environment } from 'src/environments/environment';

export interface CreateComment
{
  postId: number,
  userId: number,
  commentText: string
}

export enum ReactType {
  love = "love",
  like = "like",
  smile = "smile"
}

@Injectable({
  providedIn: 'root'
})
export class ActivityFeedService {

  readonly doamin = environment.domain

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  async reactPost(postId: number, reactType: 'like'|'smile'|'love') {
    let URL_extention = '/posts/'+postId+'/'+reactType;
    let response = await lastValueFrom(this.http.put(this.doamin+URL_extention, this.httpOptions));

    return response;
  }

  async updateComment(commentId: number, commentText: string) {
    let URL_extention = '/comments/'+commentId;
    let payload = {
      "text": commentText,

    }
    let response = await lastValueFrom(this.http.put<number>(this.doamin+URL_extention, payload, this.httpOptions));

    return response;
  }

  async createComment(postId: number, commentText: string) {
    let payload = {
      "postId": postId,
      "text": commentText
    }
    let response = await lastValueFrom(this.http.post<number>(this.doamin+'/comments', payload, this.httpOptions));

    return response;
  }

}
