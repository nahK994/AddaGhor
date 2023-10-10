import { Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { User } from '../../../user/user.service';
import { ActivityFeed } from '../../../home/home.service'
import { ActivityFeedService, ReactType } from './activity-feed.service';
import { EditedTextOutputFormat } from '../edit-item/edit-item.component';

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

  reactType = ReactType
  reactTypes = [ReactType.smile, ReactType.like, ReactType.love]
  reactEmoji = {
    "love": "heartpulse",
    "like": "thumbsup",
    "smile": "smiley"
  }

  activityFeed: ActivityFeed;
  @Input('activityFeed') set setActivityFeed(val: ActivityFeed) {
    if(!val) {
      return;
    }
    this.activityFeed = val;
  }

  @Input('user') user: User;

  commentBoxFormControl = new FormControl();

  // post: FormControl = new FormControl();
  // commentFormControl: FormControl = new FormControl();

  // isPostEditMode: boolean = false;
  // commentEditModeId: number = -1;

  constructor(
    private _activityFeedService: ActivityFeedService
  ) { }

  async reactPost(reactType: ReactType.like | ReactType.smile | ReactType.love) {
    await this._activityFeedService.reactPost(this.activityFeed.post.postId, reactType);
    if(this.activityFeed.userReact !== null && reactType === this.activityFeed.userReact) {
      this.activityFeed.reactCount[reactType]--;
      this.activityFeed.userReact = null;
    }
    else {
      this.activityFeed.reactCount[reactType]++;
      this.activityFeed.reactCount[this.activityFeed.userReact]--;
      this.activityFeed.userReact = reactType;
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
      text: this.commentBoxFormControl.value,
      date: ""
    })
    this.commentBoxFormControl.setValue('');
  }

  // editPost() {
  //   this.post.setValue(this.activityFeed.post.postId);
  //   this.isPostEditMode = true;
  // }

  // editComment(comment: Comment) {
  //   this.commentFormControl.setValue(comment.text);
  //   this.commentEditModeId = comment.commentId;
  // }

  async updateComment(editedItem: EditedTextOutputFormat) {
    await this._activityFeedService.updateComment(editedItem.itemId, editedItem.text);
    for(let i=0 ; i<this.activityFeed.comments.length; i++) {
      if(editedItem.itemId === this.activityFeed.comments[i].commentId) {
        this.activityFeed.comments[i].text = editedItem.text;
        break
      }
    }
  }

  async updatePost(editedItem: EditedTextOutputFormat) {
    await this._activityFeedService.updatePost(editedItem.itemId, editedItem.text)
    this.activityFeed.post.text = editedItem.text;
  }

}
