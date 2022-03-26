import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';
import {MatButtonModule} from '@angular/material/button';
import {MatDialogModule} from '@angular/material/dialog';
import {MatDividerModule} from '@angular/material/divider';
import {MatIconModule} from '@angular/material/icon';
import { UserRoutingModule } from './user-routing.module';
import { UserService } from './user.service';
import { ProfileComponent } from './profile/profile.component';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
@NgModule({
  declarations: [LoginComponent, RegistrationComponent, ProfileComponent],
  imports: [
    CommonModule,
    MatButtonModule,
    MatDialogModule,
    MatDividerModule,
    MatIconModule,
    UserRoutingModule,
    HttpClientModule,
    ReactiveFormsModule
  ],
  exports: [
    LoginComponent
  ],
  providers: [
    UserService
  ]
})
export class UserModule { }
