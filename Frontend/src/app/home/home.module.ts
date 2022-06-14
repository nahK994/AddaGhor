import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { HomeRoutingModule } from './home-routing-module';
import { HomeService } from './home.service';
import { HttpClientModule } from '@angular/common/http';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { UserModule } from '../user/user.module';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { PostModule } from '../shared/components/post/post.module';
import { PostCardModule } from '../shared/components/post-card/post-card.module';


@NgModule({
  declarations: [LandingPageComponent],
  imports: [
    CommonModule,
    HomeRoutingModule,
    HttpClientModule,
    MatIconModule,
    MatButtonModule,
    PostModule,
    UserModule,
    PostCardModule,
    MatInputModule,
    ReactiveFormsModule,
    MatCardModule
  ],
  providers: [
    HomeService
  ]
})
export class HomeModule { }
