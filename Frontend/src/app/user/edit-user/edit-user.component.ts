import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { CreateUser, User } from '../user.interface';
import { UserService } from '../user.service';

@Component({
  selector: 'app-edit-user',
  templateUrl: './edit-user.component.html',
  styleUrls: ['./edit-user.component.scss']
})
export class EditUserComponent implements OnInit {

  userId: number;
  user: User;

  constructor(
    private _activateRoute: ActivatedRoute,
    private _userService: UserService,
    private _router: Router,
    private _fb: FormBuilder
  ) { }

  async ngOnInit(): Promise<void> {
    this.userId = this._activateRoute.snapshot.params['userId'];
    this.user = await this._userService.getUser(this.userId);
  }

  goToHome() {
    this._router.navigate(['home', this.userId])
  }

  submit(userInfo: CreateUser) {
    try {
      this._userService.updateUser(this.userId, userInfo)
      this._router.navigate(['..'], {
        relativeTo: this._activateRoute
      })
    }
    catch(error) {
      console.log(error)
    }
  }

}
