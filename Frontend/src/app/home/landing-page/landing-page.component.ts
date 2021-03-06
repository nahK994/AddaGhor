import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { CommentEvent, UpdateCommentOutput, UpdatePostOutput } from 'src/app/shared/components/post-card/post-card.component';
import { User } from 'src/app/user/user.interface';
import { UserService } from 'src/app/user/user.service';
import { CreatePost, CreatePostComment, Timeline } from '../home.interface';
import { HomeService } from '../home.service';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {

  user: User;
  timelines: Timeline[];
  seeAllTimelines: boolean = true;
  timelinesToDisplay: Timeline[];

  constructor(
    public dialog: MatDialog,
    private _homeService: HomeService,
    private _activateRoute: ActivatedRoute,
    private _userService: UserService,
    private _router: Router
  ) { }

  async ngOnInit(): Promise<void> {
    let userId = this._activateRoute.snapshot.params['userId'];
    this._homeService.loggedInUserInfo = await this._userService.getUser(userId);
    this.user = this._homeService.loggedInUserInfo;
    this.timelines = await this._homeService.getTimelines();
    this.timelines.sort((timeline1: Timeline, timeline2: Timeline) => {
      if (new Date(timeline1.postDateTime) > new Date(timeline2.postDateTime)) {
        return -1;
      }
      else if (new Date(timeline1.postDateTime) < new Date(timeline2.postDateTime)) {
        return 1;
      }
      return 0;
    });
    this.updateTimelines();
  }

  async filterPosts() {
    this.seeAllTimelines = false;
    this.updateTimelines();
  }

  async allPosts() {
    this.seeAllTimelines = true;
    this.updateTimelines();
  }

  updateTimelines() {
    if (this.seeAllTimelines) {
      this.timelinesToDisplay = [...this.timelines]
    }
    else {
      let timelinesToDisplay = [];
      for (let item of this.timelines) {
        if (item.userId === this._homeService.loggedInUserInfo.userId) {
          timelinesToDisplay.push(item);
        }
      }
      this.timelinesToDisplay = timelinesToDisplay;
    }
  }

  async submitPost(post: string) {
    let createPostPayload: CreatePost = {
      userId: this._homeService.loggedInUserInfo.userId,
      postText: post
    }

    try {
      let res = await this._homeService.createPost(createPostPayload);
      let timelines = [...this.timelines]
      timelines.unshift({
        comments: [],
        likeReactCount: 0,
        loveReactCount: 0,
        smileReactCount: 0,
        postDateTime: res.postDateTime,
        postText: res.postText,
        postId: res.postId,
        userId: res.userId,
        userName: this._homeService.loggedInUserInfo.userName,
        avatar: this._homeService.loggedInUserInfo.avatar
      })

      this.timelines = timelines;
      this.updateTimelines();
    }
    catch (err) {

    }
  }

  async updateReactForPost(postId: number, reactType: 'like' | 'love' | 'smile') {
    try {
      await this._homeService.reactPost(postId, reactType);
      for (let item of this.timelines) {
        if (item.postId === postId) {
          if (reactType === 'like') {
            item.likeReactCount += 1;
          }
          else if (reactType === 'love') {
            item.loveReactCount += 1;
          }
          else {
            item.smileReactCount += 1;
          }
          break;
        }
        this.updateTimelines();
      }
    }
    catch (error) {
      console.log(error)
    }
  }

  async love(postId: number) {
    this.updateReactForPost(postId, 'love');
  }

  async like(postId: number) {
    this.updateReactForPost(postId, 'like');
  }

  async smile(postId: number) {
    this.updateReactForPost(postId, 'smile');
  }

  async comment(commentOutput: CommentEvent) {
    let payload: CreatePostComment = {
      postId: commentOutput.postId,
      commentText: commentOutput.commentText,
      userId: this._homeService.loggedInUserInfo.userId
    }

    try {
      let res = await this._homeService.createComment(payload);

      let timelines = [...this.timelines]
      for (let item of timelines) {
        if (item.postId === payload.postId) {
          item.comments.push({
            userId: this._homeService.loggedInUserInfo.userId,
            commentDateTime: res.commentDateTime,
            commentId: res.commentId,
            commentText: res.commentText,
            userName: this._homeService.loggedInUserInfo.userName,
            avatar: res.avatar
          });
          break;
        }
      }

      this.timelines = timelines;
      this.updateTimelines();
    }
    catch (error) {
      console.log(error)
    }
  }

  async updatePost(post: UpdatePostOutput) {
    try {
      await this._homeService.updatePost(post.postId, post.postInfo);
      for (let item of this.timelines) {
        if (item.postId === post.postId) {
          item.postText = post.postInfo.postText;
          break;
        }
      }
      this.updateTimelines();
    }
    catch (error) {
      console.log(error)
    }
  }

  async updateComment(comment: UpdateCommentOutput) {
    try {
      let isCommentUpdated = false;
      await this._homeService.updateComment(comment.commentId, comment.commentInfo);
      for (let item of this.timelines) {
        for (let itemComment of item.comments) {
          if (itemComment.commentId === comment.commentId) {
            itemComment.commentText = comment.commentInfo.commentText;
            isCommentUpdated = true;
            break;
          }
        }
        if(isCommentUpdated) {
          break;
        }
      }
      this.updateTimelines();
    }
    catch (error) {
      console.log(error)
    }
  }

  goToProfile() {
    this._router.navigate(['user', 'user-profile', this.user.userId])
  }

  logout() {
    this._router.navigate([''], {
      relativeTo: this._activateRoute
    })
  }
}
