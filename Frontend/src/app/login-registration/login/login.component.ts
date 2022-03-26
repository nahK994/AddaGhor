import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from 'src/app/user/user.service';
import { RegistrationComponent } from '../registration/registration.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup;
  constructor(
    private _router: Router,
    public dialog: MatDialog,
    private _formBuilder: FormBuilder,
    private _activatedRoute: ActivatedRoute,
    private _userService: UserService
  ) {
    this.loginForm = this._formBuilder.group({
      email: '',
      password: ''
    })
   }

  ngOnInit(): void {
  }

  createAccount(): void{
    const dialogRef = this.dialog.open(RegistrationComponent, {
      width: '400px',
      height: '450px'
    });

    dialogRef.afterClosed().subscribe(result => {
      ///Call Api Using this result data to create new account
    });
  }

  async onSubmit(){
    let userId = await this._userService.loginUser({
      email: this.loginForm.get('email').value,
      password: this.loginForm.get('password').value
    })

    this._router.navigate(['..', 'user', 'user-profile', userId], {
      relativeTo: this._activatedRoute
    })
  }

  get userDataMatched(): boolean {
    ///call api with this form data to match this user for login

    return (this.loginForm.get('emailOrPhone')?.value == 'admin' &&
            this.loginForm.get('password')?.value == 'admin');
  }

}
