import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
// import { PostInfo } from 'src/app/shared/components/post/post.component';
import { User } from 'src/app/user/user.service';
import { UserService } from 'src/app/user/user.service';
import { ActivityFeed } from '../home.service';
import { HomeService } from '../home.service';
import { FormControl } from '@angular/forms';
import { lastValueFrom } from 'rxjs';
import { debug } from 'console';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {

  user: User;
  activityFeed: ActivityFeed[];
  postText: FormControl = new FormControl('');

  constructor(
    private _homeService: HomeService,
    private _activateRoute: ActivatedRoute,
    private _userService: UserService,
    private _router: Router
  ) { }

  async ngOnInit(): Promise<void> {
    let userId = this._activateRoute.snapshot.params['userId'];
    this.user = await this._userService.getUser(userId);
    this.activityFeed = await this._homeService.getActivityFeed();
  }

  async submitPost() {
    let postId = await this._homeService.createPost(this.postText.value);

    this.activityFeed.unshift({
      post: {
        postId: postId,
        author:{
          name: this.user.name,
          profilePic: this.user.profilePicture,
          userId: this.user.userId
        },
        text: this.postText.value,
      },
      comments: [],
      reactCount: {
        like: 0,
        love: 0,
        smile: 0
      }
    })
    
    this.postText.setValue('');
  }

  goToProfile() {
    this._router.navigate(['user', 'user-profile', this.user.userId])
  }

  logout() {
    this._router.navigate([''], {
      relativeTo: this._activateRoute
    })
  }

  // async onSubmitPost() {
  //   let postId = await this._homeService.createPost(this.postText.value);

  //   this.activityFeed.unshift({
  //     post: {
  //       postId: postId,
  //       author:{
  //         name: this.user.name,
  //         profilePic: this.user.profilePicture,
  //         userId: this.user.userId
  //       },
  //       text: this.postText.value.text,
  //     },
  //     comments: [],
  //     reactCount: {
  //       like: 0,
  //       love: 0,
  //       smile: 0
  //     }
  //   })
  // }
}