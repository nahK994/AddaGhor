import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { UserRoutingModule } from './user-routing.module';
import { UserService } from './user.service';
import { ProfileComponent } from './profile/profile.component';
import { HttpClientModule } from '@angular/common/http';
import { EditUserComponent } from './edit-user/edit-user.component';
import { MatButtonModule } from '@angular/material/button';
import { UserInfoActionModule } from '../shared/components/user-info-action/user-info-action.module';
import { CreateUserComponent } from './create-user/create-user.component';
@NgModule({
  declarations: [ProfileComponent, EditUserComponent, CreateUserComponent],
  imports: [
    CommonModule,
    MatDialogModule,
    MatDividerModule,
    MatIconModule,
    UserRoutingModule,
    HttpClientModule,
    UserInfoActionModule,
    MatButtonModule
  ],
  providers: [
    UserService
  ]
})
export class UserModule { }
