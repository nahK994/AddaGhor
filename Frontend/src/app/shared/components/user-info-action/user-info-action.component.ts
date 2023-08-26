import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { User } from 'src/app/user/user.service';

@Component({
  selector: 'user-info-action',
  templateUrl: './user-info-action.component.html',
  styleUrls: ['./user-info-action.component.scss']
})
export class UserInfoActionComponent {

  mode: 'create'|'edit';
  @Input('mode') set setMode(val: 'create'|'edit') {
    if(!val) {
      return;
    }

    this.mode = val;
  }
  
  @Input('data') set setData(val: User) {
    if(!val) {
      return;
    }

    this.formGroup.get('name').setValue(val.name);
    this.formGroup.get('bio').setValue(val.bio);
    this.formGroup.get('email').setValue(val.email);
    this.formGroup.get('password').setValue(val.password);
  }

  @Output() userInfo: EventEmitter<User> = new EventEmitter();

  formGroup: FormGroup;

  constructor(
    private _fb: FormBuilder
  ) {
    this.formGroup = this._fb.group({
      name: [''],
      bio: [''],
      email: [''],
      password: ['']
    })
  }

  submit() {
    this.userInfo.emit(this.formGroup.value)
  }

}
