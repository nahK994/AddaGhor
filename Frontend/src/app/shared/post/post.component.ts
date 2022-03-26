import { Component} from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent{

  constructor(
    private dialogRef: MatDialogRef<PostComponent>
  ) {}

  newPost = new FormControl();

  closeDialogue(){
    this.dialogRef.close(this.newPost);
  }

  onSubmitPost() {
    this.closeDialogue();
  }

}
