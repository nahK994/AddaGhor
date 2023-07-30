import { Component, EventEmitter, Input, Output} from '@angular/core';
import { FormControl } from '@angular/forms';
import { PostService } from './post.service';

@Component({
  selector: 'post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent {

  isCreateMode: boolean = true;
  postId: number;
  postControl = new FormControl();
  @Output() post: EventEmitter<string> = new EventEmitter<string>();

  @Input("mode") set setMode(val: "create" | "edit") {
    if(!val) {
      return;
    }
    this.isCreateMode = val !== "create";
  }

  @Input("postInfo") set setPostText(val: {
    "postId": number,
    "postText": string
  }) {
    if(!val) {
      return;
    }
    this.postControl.setValue(val.postText);
    this.postId = val.postId;
  }

  constructor(
    private _postService: PostService
  ) {}

  async onSubmitPost() {
    if(this.isCreateMode) {
      await this._postService.createPost(this.postControl.value);
    }
    else {
      await this._postService.updatePost(this.postId, this.postControl.value);
    }
    this.postControl.setValue('');
    this.post.emit(this.postControl.value);
  }

}
