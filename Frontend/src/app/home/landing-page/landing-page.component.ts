import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { PostComponent } from 'src/app/shared/post/post.component';
import { User } from 'src/app/user/user.interface';
import { UserService } from 'src/app/user/user.service';
import { CreatePost } from '../home.interface';
import { HomeService } from '../home.service';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {

  user: User;

  constructor(
    public dialog: MatDialog,
    private _homeService: HomeService,
    private _activateRoute: ActivatedRoute,
    private _userService: UserService
  ) { }

  async ngOnInit(): Promise<void> {
    let userId = this._activateRoute.snapshot.params['userId'];
    this._homeService.loggedInUserInfo = await this._userService.getUser(userId);
    this.user = this._homeService.loggedInUserInfo;
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
        postDateTime: (new Date()).toDateString()
      }

      try {
        let res = await this._homeService.createPost(createPostPayload);
        console.log("HaHa hihi ==> ", res)
      }
      catch(err) {

      }
      console.log(result.value);
    });
  }

}
