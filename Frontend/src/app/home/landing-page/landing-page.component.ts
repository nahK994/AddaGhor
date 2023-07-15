import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from 'src/app/user/user.interface';
import { UserService } from 'src/app/user/user.service';
import { ActivityFeed } from '../home.service';
import { HomeService } from '../home.service';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {

  user: User;
  activityFeed: ActivityFeed[];
  allActivityFeed: ActivityFeed[];
  seeAllActivityFeed: boolean = true;

  constructor(
    public dialog: MatDialog,
    private _homeService: HomeService,
    private _activateRoute: ActivatedRoute,
    private _userService: UserService,
    private _router: Router
  ) { }

  async ngOnInit(): Promise<void> {
    let userId = this._activateRoute.snapshot.params['userId'];
    // this.user = await this._userService.getUser(userId);
    // this.activityFeed = await this._homeService.getActivityFeed();

    this.user = {
      email: "asd",
      profilePicture: "sdf",
      userId: 1,
      userName: "asd",
      bio: "sdf"
    }

    this.activityFeed = [
      {
        post: {
          postId: 0,
          text: "haha",
          author: {
            name: "sdf",
            profilePic: "https://c4.wallpaperflare.com/wallpaper/65/932/27/anime-demon-slayer-kimetsu-no-yaiba-boy-earrings-kimetsu-no-yaiba-hd-wallpaper-preview.jpg",
            userId: 1
          },
          visibility: "d"
        },
        comments: [
          {
            author: {
              name: "asd",
              profilePic: "https://c4.wallpaperflare.com/wallpaper/65/932/27/anime-demon-slayer-kimetsu-no-yaiba-boy-earrings-kimetsu-no-yaiba-hd-wallpaper-preview.jpg",
              userId: 2
            },
            commentId: 0,
            text: "hahyerg eg"
          },
          {
            author: {
              name: "Author",
              profilePic: "https://c4.wallpaperflare.com/wallpaper/65/932/27/anime-demon-slayer-kimetsu-no-yaiba-boy-earrings-kimetsu-no-yaiba-hd-wallpaper-preview.jpg",
              userId: 1
            },
            commentId: 1,
            text: "hahyerg eg author"
          }
        ],
        replies: [],
        react: {
          like: 0,
          love: 0,
          smile: 0
        }
      }
    ]
  }

  // async filterMyPosts() {
  //   this.seeAllTimelines = false;
  //   this.updateTimelines();
  // }

  // async allPosts() {
  //   this.seeAllTimelines = true;
  //   this.updateTimelines();
  // }

  // updateTimelines() {
  //   if (this.seeAllTimelines) {
  //     this.timelinesToDisplay = [...this.timelines]
  //   }
  //   else {
  //     let timelinesToDisplay = [];
  //     for (let item of this.timelines) {
  //       if (item.userId === this._homeService.loggedInUserInfo.userId) {
  //         timelinesToDisplay.push(item);
  //       }
  //     }
  //     this.timelinesToDisplay = timelinesToDisplay;
  //   }
  // }

  async submitPost(post: string) {
    // let createPostPayload: CreatePost = {
    //   userId: this._homeService.loggedInUserInfo.userId,
    //   postText: post
    // }

    // try {
    //   let res = await this._homeService.createPost(createPostPayload);
    //   let timelines = [...this.timelines]
    //   timelines.unshift({
    //     comments: [],
    //     likeReactCount: 0,
    //     loveReactCount: 0,
    //     smileReactCount: 0,
    //     postDateTime: res.postDateTime,
    //     postText: res.postText,
    //     postId: res.postId,
    //     userId: res.userId,
    //     userName: this._homeService.loggedInUserInfo.userName,
    //     avatar: this._homeService.loggedInUserInfo.profilePicture
    //   })

    //   this.timelines = timelines;
    //   this.updateTimelines();
    // }
    // catch (err) {

    // }
  }

  // async comment(commentOutput: CommentEvent) {
  //   let payload: CreatePostComment = {
  //     postId: commentOutput.postId,
  //     commentText: commentOutput.commentText,
  //     userId: this._homeService.loggedInUserInfo.userId
  //   }

  //   try {
  //     let res = await this._homeService.createComment(payload);

  //     let timelines = [...this.timelines]
  //     for (let item of timelines) {
  //       if (item.postId === payload.postId) {
  //         item.comments.push({
  //           userId: this._homeService.loggedInUserInfo.userId,
  //           commentDateTime: res.commentDateTime,
  //           commentId: res.commentId,
  //           commentText: res.commentText,
  //           userName: this._homeService.loggedInUserInfo.userName,
  //           avatar: res.avatar
  //         });
  //         break;
  //       }
  //     }

  //     this.timelines = timelines;
  //     this.updateTimelines();
  //   }
  //   catch (error) {
  //     console.log(error)
  //   }
  // }

  // async updatePost(post: UpdatePostOutput) {
  //   try {
  //     await this._homeService.updatePost(post.postId, post.postInfo);
  //     for (let item of this.timelines) {
  //       if (item.postId === post.postId) {
  //         item.postText = post.postInfo.postText;
  //         break;
  //       }
  //     }
  //     this.updateTimelines();
  //   }
  //   catch (error) {
  //     console.log(error)
  //   }
  // }

  // async updateComment(comment: UpdateCommentOutput) {
  //   try {
  //     let isCommentUpdated = false;
  //     await this._homeService.updateComment(comment.commentId, comment.commentInfo);
  //     for (let item of this.timelines) {
  //       for (let itemComment of item.comments) {
  //         if (itemComment.commentId === comment.commentId) {
  //           itemComment.commentText = comment.commentInfo.commentText;
  //           isCommentUpdated = true;
  //           break;
  //         }
  //       }
  //       if(isCommentUpdated) {
  //         break;
  //       }
  //     }
  //     this.updateTimelines();
  //   }
  //   catch (error) {
  //     console.log(error)
  //   }
  // }

  goToProfile() {
    this._router.navigate(['user', 'user-profile', this.user.userId])
  }

  logout() {
    this._router.navigate([''], {
      relativeTo: this._activateRoute
    })
  }
}