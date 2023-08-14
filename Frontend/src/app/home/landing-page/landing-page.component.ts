import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from 'src/app/user/user.service';
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
          date: ""
        },
        comments: [
          {
            author: {
              name: "asd",
              profilePic: "https://c4.wallpaperflare.com/wallpaper/65/932/27/anime-demon-slayer-kimetsu-no-yaiba-boy-earrings-kimetsu-no-yaiba-hd-wallpaper-preview.jpg",
              userId: 1
            },
            commentId: 0,
            text: "hahyerg eg",
            date: ""
          },
          {
            author: {
              name: "Author",
              profilePic: "https://c4.wallpaperflare.com/wallpaper/65/932/27/anime-demon-slayer-kimetsu-no-yaiba-boy-earrings-kimetsu-no-yaiba-hd-wallpaper-preview.jpg",
              userId: 2
            },
            commentId: 1,
            text: "hahyerg eg author",
            date: ""
          }
        ],
        react: {
          like: 0,
          love: 0,
          smile: 0
        }
      }
    ]
  }

  async submitPost(post: string) {
    this.activityFeed.unshift({
      post: {
        postId: 0,
        author:{
          name: this.user.name,
          profilePic: this.user.profilePicture,
          userId: this.user.userId
        },
        text: post,
        date: ""
      },
      comments: [],
      react: {
        like: 0,
        love: 0,
        smile: 0
      }
    })
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