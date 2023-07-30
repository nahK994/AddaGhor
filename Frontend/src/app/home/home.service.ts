import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from '../user/user.interface';

interface Author {
  profilePic: string,
  name: string,
  userId: number
}

export interface Post {
  postId: number,
  text: string,
  author: Author,
  visibility: string
}

export interface Comment {
  commentId: number,
  author: Author,
  text: string,
}

export interface React {
  smile: number,
  love: number,
  like: number
}

export interface Reply {
  referenceId: number,
  text: string,
  author: Author
}

export interface ActivityFeed {
  post: Post,
  comments: Comment[],
  react: React,
  replies: Reply[]
}

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  loggedInUserInfo: User;

  baseUrl_Post: string = 'http://localhost:8001';
  baseUrl_React: string = 'http://localhost:8002';
  baseUrl_Comment: string = 'http://localhost:8003';
  baseUrl_Timeline: string = 'http://localhost:8004';

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  async getPost(postId: number) {
    let URL_extention = '/posts/'+postId;
    let response = await this.http.get<Post>(this.baseUrl_Post+URL_extention, this.httpOptions).toPromise();

    return response;
  }

  async getActivityFeed() {
    let response = await this.http.get<ActivityFeed[]>(this.baseUrl_Timeline+'/timeline/all', this.httpOptions).toPromise();

    return response;
  }

  async getUserTimelines(userId: number) {
    let URL_extention = '/timeline/'+userId;
    let response = await this.http.get<ActivityFeed[]>(this.baseUrl_Timeline+URL_extention, this.httpOptions).toPromise();

    return response;
  }
}
