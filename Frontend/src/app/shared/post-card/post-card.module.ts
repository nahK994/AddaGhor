import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PostCardComponent } from './post-card.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AngularEmojisModule } from 'angular-emojis';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';



@NgModule({
  declarations: [PostCardComponent],
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule,
    AngularEmojisModule,
    ReactiveFormsModule,
    FormsModule
  ],
  exports: [
    PostCardComponent
  ]
})
export class PostCardModule { }
