import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PostComponent } from './post.component';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';


@NgModule({
  declarations: [PostComponent],
  imports: [
    CommonModule,
    MatDividerModule,
    MatButtonModule,
    ReactiveFormsModule
  ],
  exports: [
    PostComponent
  ]
})
export class PostModule { }
