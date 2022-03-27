import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { CreatePostComment, Timeline } from 'src/app/home/home.interface';

@Component({
  selector: 'app-post-card',
  templateUrl: './post-card.component.html',
  styleUrls: ['./post-card.component.scss']
})
export class PostCardComponent implements OnInit {

  timeLineInfo: Timeline;
  @Input() set setTimeLineInfo(val: Timeline) {
    if(!val) {
      return;
    }
    this.timeLineInfo = val;
  }
  @Output() likeEvent: EventEmitter<number> = new EventEmitter();
  @Output() smileEvent: EventEmitter<number> = new EventEmitter();
  @Output() loveEvent: EventEmitter<number> = new EventEmitter();

  @Output() commentEvent: EventEmitter<CreatePostComment> = new EventEmitter();

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
      userId: this.timeLineInfo.userId,
      userName: this.timeLineInfo.userName,
      commentText: this.newComment.value,
      commentDateTime: (new Date()).toUTCString()
    })
  }

}
