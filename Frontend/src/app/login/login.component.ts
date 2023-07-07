import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
// import { AppService } from '../app.service';

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
    // private _appService: AppService
  ) {
    this.loginForm = this._formBuilder.group({
      email: [''],
      password: ['']
    })
   }

  createAccount(): void{
    this._router.navigate(['user/create'])
  }

  async login(){
    // try {
    //   let userId = await this._appService.loginUser({
    //     email: this.loginForm.get('email').value,
    //     password: this.loginForm.get('password').value
    //   })
  
    //   this._router.navigate(['home', userId])
    // }
    // catch(error) {
    //   console.log("haha ==> ", error)
    // }

    this._router.navigate(['home', 1])
  }

}
