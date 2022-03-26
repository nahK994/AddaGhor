import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

  signUpForm: FormGroup;

  constructor(
    private dialogRef: MatDialogRef<RegistrationComponent>,
    private _formBuilder: FormBuilder
  ) {
    this.signUpForm = this._formBuilder.group({
      firstName: '',
      lastName: '',
      email: '',
      newPassword: '',
      confirmNewPassword: ''
    })
  }

  ngOnInit(): void {
  }

  closeWindow() {
    this.dialogRef.close(this.signUpForm);
  }

  submitSignUpFormData() {
    this.closeWindow();
  }

}
