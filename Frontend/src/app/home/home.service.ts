import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { User } from '../user/user.service';
import { lastValueFrom } from 'rxjs';

interface Author {
  profilePic: string,
  name: string,
  userId: number
}

export interface Post {
  postId?: number,
  text: string,
  author: Author,
  date?: string
}

export interface Comment {
  commentId?: number,
  author: Author,
  text: string,
  date?: string
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
  userReact?: string
}

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  loggedInUserInfo: User;
  readonly commandDomain = environment.commandDomain
  readonly queryDomain = environment.queryDomain

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  async getPost(postId: number) {
    let URL_extention = '/posts/'+postId;
    let response = await lastValueFrom(this.http.get<Post>(this.commandDomain+URL_extention, this.httpOptions));

    return response;
  }

  async getActivityFeed() {
    let response = await lastValueFrom(this.http.get<ActivityFeed[]>(this.queryDomain+'/activity', this.httpOptions));

    return response;
  }

  async getUserTimelines(userId: number) {
    let URL_extention = '/timeline/'+userId;
    let response = await lastValueFrom(this.http.get<ActivityFeed[]>(this.queryDomain+URL_extention, this.httpOptions));

    return response;
  }

  // async updatePost(postId: number, postText: string) {
  //   let payload = {
  //     "text": postText
  //   }
  //   let URL_extention = '/posts/'+postId;
  //   let response = await lastValueFrom(this.http.put<number>(this.commandDomain+URL_extention, payload, this.httpOptions));

  //   return response;
  // }

  async createPost(postText: string) {
    let payload = {
      "text": postText
    };
    let response = await lastValueFrom(this.http.post<{id: number}>(this.commandDomain+'/posts', payload, this.httpOptions));

    return response.id;
  }
}
