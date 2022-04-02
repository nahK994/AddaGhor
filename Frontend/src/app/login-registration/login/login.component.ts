import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from 'src/app/user/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  loginForm: FormGroup;
  constructor(
    private _router: Router,
    private _formBuilder: FormBuilder,
    private _activatedRoute: ActivatedRoute,
    private _userService: UserService
  ) {
    this.loginForm = this._formBuilder.group({
      email: [''],
      password: ['']
    })
   }

  createAccount(): void{
    this._router.navigate(['user/create'])
  }

  async onSubmit(){
    try {
      let userId = await this._userService.loginUser({
        email: this.loginForm.get('email').value,
        password: this.loginForm.get('password').value
      })
  
      this._router.navigate(['..', 'home', userId], {
        relativeTo: this._activatedRoute
      })
    }
    catch(error) {
      console.log("haha ==> ", error)
    }
  }

}
