import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';
import {MatButtonModule} from '@angular/material/button';



@NgModule({
  declarations: [LoginComponent, RegistrationComponent],
  imports: [
    CommonModule,
    MatButtonModule,
  ],
  exports: [
    LoginComponent
  ]
})
export class LoginRegistrationSectioinModule { }
