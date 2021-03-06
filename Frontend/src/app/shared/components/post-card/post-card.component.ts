import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { CreatePost, CreatePostComment, PostComment, Timeline } from 'src/app/home/home.interface';

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
export class PostCardComponent implements OnInit {

  timeLineInfo: Timeline;
  @Input('timeLineInfo') set setTimeLineInfo(val: Timeline) {
    if(!val) {
      return;
    }
    this.timeLineInfo = val;
  }

  @Input('userId') userId: number;

  @Output() likeEvent: EventEmitter<number> = new EventEmitter();
  @Output() smileEvent: EventEmitter<number> = new EventEmitter();
  @Output() loveEvent: EventEmitter<number> = new EventEmitter();

  @Output() commentEvent: EventEmitter<CommentEvent> = new EventEmitter();

  @Output() updatePost: EventEmitter<UpdatePostOutput> = new EventEmitter();
  @Output() updateComment: EventEmitter<UpdateCommentOutput> = new EventEmitter();

  newComment = new FormControl();

  post: FormControl = new FormControl();
  comment: FormControl = new FormControl();

  isPostEditMode: boolean;
  isCommentEditMode: boolean;
  commentInfoToUpdate: PostComment;

  constructor() { }

  ngOnInit(): void {
  }

  likeReact() {
    this.likeEvent.emit(this.timeLineInfo.postId);
  }

  smileReact() {
    this.smileEvent.emit(this.timeLineInfo.postId);
  }

  loveReact() {
    this.loveEvent.emit(this.timeLineInfo.postId);
  }

  commentPost() {
    this.commentEvent.emit({
      postId: this.timeLineInfo.postId,
      commentText: this.newComment.value
    })
    this.newComment.setValue('');
  }

  editPost() {
    this.post.setValue(this.timeLineInfo.postText);
    this.isPostEditMode = true;
  }

  submitPost() {
    this.isPostEditMode = false;
    this.updatePost.emit({
      postId: this.timeLineInfo.postId,
      postInfo: {
        userId: this.userId,
        postText: this.post.value
      }
    })
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
        postId: this.timeLineInfo.postId,
        userId: this.userId,
        commentText: this.comment.value
      }
    })
  }

  onUpdatePost(post: string) {
    this.updatePost.emit({
      postId: this.timeLineInfo.postId,
      postInfo: {
        userId: this.timeLineInfo.userId,
        postText: post
      }
    })
    this.isPostEditMode = false;
  }

}
