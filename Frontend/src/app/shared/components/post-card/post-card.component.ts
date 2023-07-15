import { Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivityFeed, Comment } from '../../../home/home.service'
import { PostCardService } from './post-card.service';

export interface CommentEvent {
  postId: number;
  commentText: string;
}

@Component({
  selector: 'post-card',
  templateUrl: './post-card.component.html',
  styleUrls: ['./post-card.component.scss']
})
export class PostCardComponent {

  activityFeed: ActivityFeed;
  @Input('activityFeed') set setActivityFeed(val: ActivityFeed) {
    if(!val) {
      return;
    }
    this.activityFeed = val;
  }

  @Input('userId') userId: number;

  commentBoxFormControl = new FormControl();

  post: FormControl = new FormControl();
  commentFormControl: FormControl = new FormControl();

  isPostEditMode: boolean;
  commentEditModeId: number = -1;

  
  // commentInfoToUpdate: PostComment;

  constructor(
    private _postCardService: PostCardService
  ) { }

  async reactPost(reactType: 'like'|'smile'|'love') {
    await this._postCardService.reactPost(this.activityFeed.post.postId, reactType);
  }

  async createComment() {
    await this._postCardService.createComment(this.activityFeed.post.postId, this.commentBoxFormControl.value);
    this.commentBoxFormControl.setValue('');
  }

  editPost() {
    this.post.setValue(this.activityFeed.post.postId);
    this.isPostEditMode = true;
  }

  editComment(comment: Comment) {
    this.commentFormControl.setValue(comment.text);
    // this.commentInfoToUpdate = comment
    this.commentEditModeId = comment.commentId;
  }

  async updateComment(comment: Comment) {
    await this._postCardService.updateComment(comment.commentId, this.commentFormControl.value);
    this.commentEditModeId = -1;
  }

  async updatePost(postText: string) {
    try {
      await this._postCardService.updatePost(this.activityFeed.post.postId, postText);
      this.activityFeed.post.text = postText;
    }
    catch (error) {
      console.log(error)
    }
  }

}
