import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { UserRoutingModule } from './user-routing.module';
import { UserService } from './user.service';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { EditUserComponent } from './edit-user/edit-user.component';
import { MatButtonModule } from '@angular/material/button';
import { UserInfoActionModule } from '../shared/components/user-info-action/user-info-action.module';
import { CreateUserComponent } from './create-user/create-user.component';
import { AccessTokenInterceptor } from '../interceptor/token.interceptor';
import { ActivateUserComponent } from './activate-user/activate-user.component';
@NgModule({
  declarations: [EditUserComponent, CreateUserComponent, ActivateUserComponent],
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
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AccessTokenInterceptor,
      multi: true
    },
    UserService
  ]
})
export class UserModule { }
