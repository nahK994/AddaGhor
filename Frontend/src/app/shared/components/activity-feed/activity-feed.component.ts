import { Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivityFeed, Comment } from '../../../home/home.service'
import { ActivityFeedService } from './activity-feed.service';

export interface CommentEvent {
  postId: number;
  commentText: string;
}

@Component({
  selector: 'activity-feed',
  templateUrl: './activity-feed.component.html',
  styleUrls: ['./activity-feed.component.scss']
})
export class ActivityFeedComponent {

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
    private _activityFeedService: ActivityFeedService
  ) { }

  async reactPost(reactType: 'like'|'smile'|'love') {
    await this._activityFeedService.reactPost(this.activityFeed.post.postId, reactType);
  }

  async createComment() {
    await this._activityFeedService.createComment(this.activityFeed.post.postId, this.commentBoxFormControl.value);
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
    await this._activityFeedService.updateComment(comment.commentId, this.commentFormControl.value);
    this.commentEditModeId = -1;
  }

  async updatePost(postText: string) {
    try {
      await this._activityFeedService.updatePost(this.activityFeed.post.postId, postText);
      this.activityFeed.post.text = postText;
    }
    catch (error) {
      console.log(error)
    }
  }

}
