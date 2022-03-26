import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { HomeRoutingModule } from './home-routing-module';
import { HomeService } from './home.service';
import { HttpClientModule } from '@angular/common/http';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { PostModule } from '../shared/post/post.module';
import { MatDialogModule } from '@angular/material/dialog';
import { UserModule } from '../user/user.module';

@NgModule({
  declarations: [LandingPageComponent],
  imports: [
    CommonModule,
    HomeRoutingModule,
    HttpClientModule,
    MatIconModule,
    MatButtonModule,
    PostModule,
    MatDialogModule,
    UserModule
  ],
  providers: [
    HomeService
  ]
})
export class HomeModule { }
