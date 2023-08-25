import { Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { User } from '../../../user/user.service';
import { ActivityFeed, Comment } from '../../../home/home.service'
import { ActivityFeedService, ReactType } from './activity-feed.service';

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

  isPostEditMode: boolean = false;
  commentEditModeId: number = -1;

  constructor(
    private _activityFeedService: ActivityFeedService
  ) { }

  isSameReact(reactType: ReactType.like | ReactType.smile | ReactType.love) {
    if(reactType === ReactType.like && this.activityFeed.userReact === ReactType.like) {
      return true;
    }
    else if(reactType === ReactType.love && this.activityFeed.userReact === ReactType.love) {
      return true;
    }
    else if(reactType === ReactType.smile && this.activityFeed.userReact === ReactType.smile) {
      return true;
    }
    return false;
  }

  async reactPost(reactType: ReactType.like | ReactType.smile | ReactType.love) {
    await this._activityFeedService.reactPost(this.activityFeed.post.postId, reactType);
    if(this.isSameReact(reactType)) {
      this.activityFeed.reactCount[reactType]--;
    }
    else {
      this.activityFeed.reactCount[reactType]++;
      this.activityFeed.reactCount[this.activityFeed.userReact]--;
    }

    this.activityFeed.userReact = reactType
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
