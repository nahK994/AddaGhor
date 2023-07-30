import { Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { User } from '../../../user/user.service';
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

  @Input('user') user: User;

  commentBoxFormControl = new FormControl();

  post: FormControl = new FormControl();
  commentFormControl: FormControl = new FormControl();

  isPostEditMode: boolean;
  commentEditModeId: number = -1;

  constructor(
    private _activityFeedService: ActivityFeedService
  ) { }

  async reactPost(reactType: 'like'|'smile'|'love') {
    await this._activityFeedService.reactPost(this.activityFeed.post.postId, reactType);
    if(reactType === 'like') {
      this.activityFeed.react.like++;
    }
    else if(reactType === 'love') {
      this.activityFeed.react.love++;
    }
    else {
      this.activityFeed.react.smile++;
    }
  }

  async createComment() {
    await this._activityFeedService.createComment(this.activityFeed.post.postId, this.commentBoxFormControl.value);
    this.activityFeed.comments.push({
      author: {
        name: this.user.name,
        profilePic: this.user.profilePicture,
        userId: this.user.userId
      },
      text: this.commentBoxFormControl.value
    })
    this.commentBoxFormControl.setValue('');
  }

  editPost() {
    this.post.setValue(this.activityFeed.post.postId);
    this.isPostEditMode = true;
  }

  editComment(comment: Comment) {
    this.commentFormControl.setValue(comment.text);
    this.commentEditModeId = comment.commentId;
  }

  async updateComment(comment: Comment) {
    await this._activityFeedService.updateComment(comment.commentId, this.commentFormControl.value);
    this.commentEditModeId = -1;
    for(let i=0 ; i<this.activityFeed.comments.length; i++) {
      if(comment.commentId === this.activityFeed.comments[i].commentId) {
        this.activityFeed.comments[i].text = this.commentFormControl.value;
        break
      }
    }
  }

  async updatePost(postText: string) {
    this.activityFeed.post.text = postText;
    this.isPostEditMode = false;
  }

}
