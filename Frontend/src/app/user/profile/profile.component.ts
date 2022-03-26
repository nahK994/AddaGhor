import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { User } from '../user.interface';
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
    private _userService: UserService
  ) { }

  async ngOnInit(): Promise<void> {
    let userId = this._activateRoute.snapshot.params['userId'];
    this.user = await this._userService.getUser(userId)
    this.user.email
  }

}
