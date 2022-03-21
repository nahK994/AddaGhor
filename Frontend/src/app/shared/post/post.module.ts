import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PostComponent } from './post.component';
import { PostService } from './post.service';



@NgModule({
  declarations: [PostComponent],
  imports: [
    CommonModule
  ],
  providers: [
    PostService
  ]
})
export class PostModule { }
