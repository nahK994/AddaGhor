import { Component, EventEmitter, Input, Output} from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent {

  isCreateMode: boolean = true;
  @Input("mode") set setMode(val: "create" | "edit") {
    if(!val) {
      return;
    }
    if(val !== "create") {
      this.isCreateMode = false;
    }
  }
  @Output() post: EventEmitter<string> = new EventEmitter<string>();

  constructor() {}

  postControl = new FormControl();

  onSubmitPost() {
    this.post.emit(this.postControl.value)
  }

}
