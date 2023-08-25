import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { User } from '../user/user.service';

interface Author {
  profilePic: string,
  name: string,
  userId: number
}

export interface Post {
  postId?: number,
  text: string,
  author: Author,
  date: string
}

export interface Comment {
  commentId?: number,
  author: Author,
  text: string,
  date: string
}

export interface React {
  smile: number,
  love: number,
  like: number
}

export interface ActivityFeed {
  post: Post,
  comments: Comment[],
  reactCount: React,
  userReact: string
}

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  loggedInUserInfo: User;
  readonly doamin = environment.domain

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  async getPost(postId: number) {
    let URL_extention = '/posts/'+postId;
    let response = await this.http.get<Post>(this.doamin+URL_extention, this.httpOptions).toPromise();

    return response;
  }

  async getActivityFeed() {
    let response = await this.http.get<ActivityFeed[]>(this.doamin+'/activity', this.httpOptions).toPromise();

    return response;
  }

  async getUserTimelines(userId: number) {
    let URL_extention = '/timeline/'+userId;
    let response = await this.http.get<ActivityFeed[]>(this.doamin+URL_extention, this.httpOptions).toPromise();

    return response;
  }
}
