import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivityFeed, PostComment } from 'src/app/home/home.interface';
import { CreatePost, PostCardService } from './post-card.service';

export interface CommentEvent {
  postId: number;
  commentText: string;
}

export interface UpdatePostOutput {
  postId: number;
  postInfo: CreatePost;
}

export interface UpdateCommentOutput {
  commentId: number;
  commentInfo: CreatePostComment;
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

  @Output() commentEvent: EventEmitter<CommentEvent> = new EventEmitter();

  // @Output() updatePost: EventEmitter<UpdatePostOutput> = new EventEmitter();
  @Output() updateComment: EventEmitter<UpdateCommentOutput> = new EventEmitter();

  newComment = new FormControl();

  post: FormControl = new FormControl();
  comment: FormControl = new FormControl();

  isPostEditMode: boolean;
  isCommentEditMode: boolean;
  commentInfoToUpdate: PostComment;

  constructor(
    private _postCardService: PostCardService
  ) { }

  async reactPost(reactType: 'like'|'smile'|'love') {
    await this._postCardService.reactPost(this.activityFeed.post.postId, reactType);
  }

  commentPost() {
    this.commentEvent.emit({
      postId: this.activityFeed.post.postId,
      commentText: this.newComment.value
    })
    this.newComment.setValue('');
  }

  editPost() {
    this.post.setValue(this.activityFeed.post.postId);
    this.isPostEditMode = true;
  }

  editComment(comment: PostComment) {
    this.comment.setValue(comment.commentText);
    this.commentInfoToUpdate = comment
    this.isCommentEditMode = true;
  }

  submitComment() {
    this.isCommentEditMode = false;
    this.updateComment.emit({
      commentId: this.commentInfoToUpdate.commentId,
      commentInfo: {
        postId: this.activityFeed.post.postId,
        userId: this.userId,
        commentText: this.comment.value
      }
    })
  }

  // onUpdatePost(post: string) {
  //   this.updatePost.emit({
  //     postId: this.activityFeed.post.postId,
  //     postInfo: {
  //       userId: this.userId,
  //       postText: post
  //     }
  //   })
  //   this.isPostEditMode = false;
  // }
  async updatePost(post: UpdatePostOutput) {
    try {
      await this._postCardService.updatePost(post.postId, post.postInfo);
      this.activityFeed.post.text = post.postInfo.postText
    }
    catch (error) {
      console.log(error)
    }
  }

}
