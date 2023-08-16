import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { User } from '../user.service';
import { UserService } from '../user.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

  user: User;

  constructor(
    private _activateRoute: ActivatedRoute,
    private _userService: UserService,
    private _router: Router
  ) { }

  async ngOnInit(): Promise<void> {
    let userId = this._activateRoute.snapshot.params['userId'];
    this.user = await this._userService.getUser(userId)
    console.log(this.user)
  }

  goToHome() {
    this._router.navigate(['home', this.user.userId])
  }

  edit() {
    this._router.navigate(['edit'], {
      relativeTo: this._activateRoute
    })
  }
}
