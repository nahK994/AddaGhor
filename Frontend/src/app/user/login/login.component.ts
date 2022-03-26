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
    public dialog: MatDialog,
    private _router: Router,
    private _activatedRoute: ActivatedRoute,
    private _formBuilder: FormBuilder
  ) {
    this.loginForm = this._formBuilder.group({
      emailOrPhone: '',
      password: ''
    })
   }

  ngOnInit(): void {
  }

  navigateToHomePage(){
    this._router.navigate([
      '..',
      'home'
    ],
    {
      relativeTo: this._activatedRoute
    })
  }

  createAccount(): void{
    const dialogRef = this.dialog.open(RegistrationComponent, {
      width: '400px',
      height: '450px'
      // data: {name: this.name, animal: this.animal},
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      // this.animal = result;
    });
  }

  onSubmit(){
    console.log("form value", this.loginForm.value);
  }

}
