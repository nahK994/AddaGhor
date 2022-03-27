import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { CommentEvent, UpdateCommentOutput, UpdatePostOutput } from 'src/app/shared/post-card/post-card.component';
import { PostComponent } from 'src/app/shared/post/post.component';
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
    if(this.seeAllTimelines) {
      this.timelinesToDisplay = [...this.timelines]
    }
    else {
      let timelinesToDisplay = [];
      for(let item of this.timelines) {
        if(item.userId === this._homeService.loggedInUserInfo.userId) {
          timelinesToDisplay.push(item);
        }
      }
      this.timelinesToDisplay = timelinesToDisplay;
    }
  }

  openCreatePostDialogue() {
    const dialogRef = this.dialog.open(PostComponent, {
      width: '520px',
      height: '380px'
    });

    dialogRef.afterClosed().subscribe(async result => {
      ///Call Api Using this result data to create new account
      let createPostPayload: CreatePost = {
        userId: this._homeService.loggedInUserInfo.userId,
        userName: this._homeService.loggedInUserInfo.userName,
        postText: result.value,
        postDateTime: (new Date()).toUTCString()
      }

      try {
        let res = await this._homeService.createPost(createPostPayload);
        let timelines = [...this.timelines]
        timelines.push({
          comments: [],
          likeReactCount: 0,
          loveReactCount: 0,
          smileReactCount: 0,
          postDateTime: res.postDateTime,
          postText: res.postText,
          postId: res.postId,
          userId: res.userId,
          userName: res.userName
        })

        this.timelines = timelines;
        this.updateTimelines();
      }
      catch(err) {

      }
      console.log(result.value);
    });
  }

  async love(postId: number) {
    try {
      await this._homeService.reactPost(postId, 'love');
      for(let item of this.timelines) {
        if(item.postId === postId) {
          item.loveReactCount+=1;
          break;
        }
      }
      this.updateTimelines();
    }
    catch(error) {
      console.log(error)
    }
  }

  async like(postId: number) {
    try {
      await this._homeService.reactPost(postId, 'like');
      for(let item of this.timelines) {
        if(item.postId === postId) {
          item.likeReactCount+=1;
          break;
        }
      }
      this.updateTimelines();
    }
    catch(error) {
      console.log(error)
    }
  }

  async smile(postId: number) {
    try {
      await this._homeService.reactPost(postId, 'smile');
      for(let item of this.timelines) {
        if(item.postId === postId) {
          item.smileReactCount+=1;
          break;
        }
      }
      this.updateTimelines()
    }
    catch(error) {
      console.log(error)
    }
  }

  async comment(commentOutput: CommentEvent) {
    let payload: CreatePostComment = {
      postId: commentOutput.postId,
      commentText: commentOutput.commentText,
      commentDateTime: (new Date()).toUTCString(),
      userId: this._homeService.loggedInUserInfo.userId,
      userName: this._homeService.loggedInUserInfo.userName
    }

    try {
      let res = await this._homeService.createComment(payload);
      let timelines = [...this.timelines]
      for(let item of this.timelines) {
        if(item.postId === payload.postId) {
          item.comments.push({
            userId: this._homeService.loggedInUserInfo.userId,
            commentDateTime: res.commentDateTime,
            commentId: res.commentId,
            commentText: res.commentText,
            postId: res.postId,
            userName: res.userName
          });
        }
        break;
      }
      this.updateTimelines();

      this.timelines = timelines;
      this.updateTimelines();
    }
    catch(error) {
      console.log(error)
    }
  }

  async updatePost(post: UpdatePostOutput) {
    try {
      let res = await this._homeService.updatePost(post.postId, post.postInfo);
      for(let item of this.timelines) {
        if(item.postId === post.postId) {
          item.postText = post.postInfo.postText;
          item.postDateTime = post.postInfo.postDateTime;
          break;
        }
      }
      this.updateTimelines();
    }
    catch(error) {
      console.log(error)
    }
  }

  async updateComment(comment: UpdateCommentOutput) {
    try {
      let res = await this._homeService.updateComment(comment.commentId, comment.commentInfo);
      for(let item of this.timelines) {
        for(let itemComment of item.comments) {
          if(itemComment.commentId === comment.commentId) {
            itemComment.commentDateTime = comment.commentInfo.commentDateTime;
            itemComment.commentText = comment.commentInfo.commentText;
          }
        }
      }
      this.updateTimelines();
    }
    catch(error) {
      console.log(error)
    }
  }

  goToProfile() {
    this._router.navigate(['user-profile', this.user.userId])
  }

  logout() {
    this._router.navigate([''], {
      relativeTo: this._activateRoute
    })
  }
}
