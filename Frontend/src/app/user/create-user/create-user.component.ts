import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { User, UserService } from '../user.service';

@Component({
  selector: 'app-create-user',
  templateUrl: './create-user.component.html',
  styleUrls: ['./create-user.component.scss']
})
export class CreateUserComponent {

  constructor(
    private _userService: UserService,
    private _router: Router
  ) { }

  async signUp(userInfo: User) {    
   try {
    await this._userService.createUser(userInfo);
    this._router.navigate([''])
   }
   catch(error) {
     console.log("error ==> ", error)
   }
  }

}
