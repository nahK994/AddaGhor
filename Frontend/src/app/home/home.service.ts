import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from '../user/user.interface';
import { CreatePostComment, PostComment, CreatePost, CreateReact, Post, Timeline } from './home.interface';

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

  async createPost(payload: CreatePost) {
    let response = await this.http.post<Post>(this.baseUrl_Post+'/post/create', payload, this.httpOptions).toPromise();

    return response;
  }

  async updatePost(postId: number, payload: CreatePost) {
    let URL_extention = '/post/update/'+postId;
    let response = await this.http.put<CreatePost>(this.baseUrl_Post+URL_extention, payload, this.httpOptions).toPromise();

    return response;
  }

  async getPost(postId: number) {
    let URL_extention = '/posts/'+postId;
    let response = await this.http.get<Post>(this.baseUrl_Post+URL_extention, this.httpOptions).toPromise();

    return response;
  }


  async createComment(payload: CreatePostComment) {
    let response = await this.http.post<PostComment>(this.baseUrl_Comment+'/comment/create', payload, this.httpOptions).toPromise();

    return response;
  }

  async updateComment(commentId: number, payload: CreatePostComment) {
    let URL_extention = '/comment/update/'+commentId;
    let response = await this.http.put<CreatePostComment>(this.baseUrl_Comment+URL_extention, payload, this.httpOptions).toPromise();

    return response;
  }

  async getComment(commentId: number) {
    let URL_extention = '/comments/'+commentId;
    let response = await this.http.get<PostComment>(this.baseUrl_Comment+URL_extention, this.httpOptions).toPromise();

    return response;
  }

  async reactPost(postId: number, reactType: 'like'|'smile'|'love') {
    let URL_extention = '/react/'+postId+'/'+reactType;
    let response = await this.http.put<CreateReact>(this.baseUrl_React+URL_extention, this.httpOptions).toPromise();

    return response;
  }

  async getTimelines() {
    let response = await this.http.get<Timeline[]>(this.baseUrl_Timeline+'/timeline/all', this.httpOptions).toPromise();

    return response;
  }

  async getUserTimelines(userId: number) {
    let URL_extention = '/timeline/'+userId;
    let response = await this.http.get<Timeline[]>(this.baseUrl_Timeline+URL_extention, this.httpOptions).toPromise();

    return response;
  }
}
