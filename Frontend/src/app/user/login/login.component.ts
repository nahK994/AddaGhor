import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
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
  ) {
    this.loginForm = this._formBuilder.group({
      emailOrPhone: '',
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

  onSubmit(){
    if(this.userDataMatched) {
      this._router.navigate(
        ['..', 'home'],
        { relativeTo: this._activatedRoute })
    }
  }

  get userDataMatched(): boolean {
    ///call api with this form data to match this user for login

    return (this.loginForm.get('emailOrPhone')?.value == 'admin' &&
            this.loginForm.get('password')?.value == 'admin');
  }

}
