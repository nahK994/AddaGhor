import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { CreateUser } from 'src/app/user/user.interface';
import { UserService } from 'src/app/user/user.service';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

  signUpForm: FormGroup;

  constructor(
    private dialogRef: MatDialogRef<RegistrationComponent>,
    private _formBuilder: FormBuilder,
    private _userService: UserService,
    private _router: Router
  ) {
    this.signUpForm = this._formBuilder.group({
      firstName: [''],
      lastName: [''],
      email: [''],
      password: [''],
      occupation: [''],
      bio: [''],
      avatar: ['']
    })
  }

  ngOnInit(): void {
  }

  async signUp() {
    let payload: CreateUser = {
      userName: this.signUpForm.get('firstName').value + ' ' + this.signUpForm.get('lastName').value,
      email: this.signUpForm.get('email').value,
      occupation: this.signUpForm.get('occupation').value,
      bio: this.signUpForm.get('bio').value,
      password: this.signUpForm.get('password').value,
      avatar: this.signUpForm.get('avatar').value
    }
    
   try {
    let response = await this._userService.createUser(payload);
    this._router.navigate(['user-profile', response.userId])

   }
   catch(error) {
     console.log("error ==> ", error)
   }
  }

  closeWindow() {
    this.dialogRef.close(this.signUpForm);
  }

  submitSignUpFormData() {
    this.closeWindow();
  }

}
