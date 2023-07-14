import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PostCardComponent } from './post-card.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AngularEmojisModule } from 'angular-emojis';
import { ReactiveFormsModule } from '@angular/forms';
import {MatCardModule} from '@angular/material/card';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import { PostModule } from '../post/post.module';
import { PostCardService } from './post-card.service';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [PostCardComponent],
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule,
    AngularEmojisModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    PostModule,
    HttpClientModule
  ],
  exports: [
    PostCardComponent
  ],
  providers: [
    PostCardService
  ]
})
export class PostCardModule { }
