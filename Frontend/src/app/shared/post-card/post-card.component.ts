import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Timeline } from 'src/app/home/home.interface';

export interface CommentEvent {
  postId: number;
  commentText: string;
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
  @Output() likeEvent: EventEmitter<number> = new EventEmitter();
  @Output() smileEvent: EventEmitter<number> = new EventEmitter();
  @Output() loveEvent: EventEmitter<number> = new EventEmitter();

  @Output() commentEvent: EventEmitter<CommentEvent> = new EventEmitter();

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

}
