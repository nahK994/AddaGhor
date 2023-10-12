import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-activate-user',
  templateUrl: './activate-user.component.html',
  styleUrls: ['./activate-user.component.scss']
})
export class ActivateUserComponent implements OnInit {

  activationCode: string;
  userId: number;
  constructor(
    private _activateRoute: ActivatedRoute,
    private _userService: UserService
  ) { }

  async ngOnInit(): Promise<void> {
    this.activationCode = this._activateRoute.snapshot.params['code'];
    this.userId = this._activateRoute.snapshot.params['userId']
    await this._userService.activateUser(this.userId, this.activationCode)
  }

}
