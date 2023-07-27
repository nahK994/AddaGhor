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
      name: "asd",
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

  goToProfile() {
    this._router.navigate(['user', 'user-profile', this.user.userId])
  }

  logout() {
    this._router.navigate([''], {
      relativeTo: this._activateRoute
    })
  }

  filterMyPosts() {
    this.seeAllActivityFeed = false;
  }

  allPosts() {
    this.seeAllActivityFeed = true;
  }  
}