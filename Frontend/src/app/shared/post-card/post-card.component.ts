import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { CreatePost, CreatePostComment, Timeline } from 'src/app/home/home.interface';

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

  @Input('userId') userId: string;

  @Output() likeEvent: EventEmitter<number> = new EventEmitter();
  @Output() smileEvent: EventEmitter<number> = new EventEmitter();
  @Output() loveEvent: EventEmitter<number> = new EventEmitter();

  @Output() commentEvent: EventEmitter<CommentEvent> = new EventEmitter();

  @Output() updatePost: EventEmitter<CreatePost> = new EventEmitter();
  @Output() updateComment: EventEmitter<CreatePostComment> = new EventEmitter();

  newComment = new FormControl();

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
  }

  editPost() {

  }

  editComment() {

  }

}
