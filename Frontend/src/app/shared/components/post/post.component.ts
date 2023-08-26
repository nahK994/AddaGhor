import { Component, EventEmitter, Input, Output} from '@angular/core';
import { FormControl } from '@angular/forms';
import { PostService } from './post.service';

export interface PostInfo {
  postId: number,
  text: string
}

@Component({
  selector: 'post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent {

  isCreateMode: boolean = true;
  postId: number;
  postText: FormControl = new FormControl('');
  @Output() post: EventEmitter<PostInfo> = new EventEmitter<PostInfo>();

  @Input("mode") set setMode(val: "create" | "edit") {
    if(!val) {
      return;
    }
    this.isCreateMode = val === "create";
  }

  @Input("postInfo") set setPostInfo(val: {
    "postId": number,
    "text": string
  }) {
    if(!val) {
      return;
    }
    this.postText.setValue(val.text);
    this.postId = val.postId;
  }

  constructor(
    private _postService: PostService
  ) {}

  async onSubmitPost() {
    let postId = -1;
    if(this.isCreateMode) {
      postId = await this._postService.createPost(this.postText.value);
    }
    else {
      postId = await this._postService.updatePost(this.postId, this.postText.value);
    }
    let postInfo: PostInfo = {
      postId: postId,
      text: this.postText.value
    }
    this.post.emit(postInfo);
    this.postText.setValue('');
  }

}
