import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { HomeRoutingModule } from './home-routing-module';
import { HomeService } from './home.service';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import {MatIconModule} from '@angular/material/icon';
import { UserModule } from '../user/user.module';
import { MatCardModule } from '@angular/material/card';
import { PostModule } from '../shared/components/post/post.module';
import { PostCardModule } from '../shared/components/post-card/post-card.module';
import { AccessTokenInterceptor } from '../interceptor/token.interceptor';
import { MatButtonModule } from '@angular/material/button';


@NgModule({
  declarations: [LandingPageComponent],
  imports: [
    CommonModule,
    HomeRoutingModule,
    HttpClientModule,
    MatIconModule,
    PostModule,
    UserModule,
    PostCardModule,
    MatCardModule,
    MatButtonModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AccessTokenInterceptor,
      multi: true
    },
    HomeService
  ]
})
export class HomeModule { }
