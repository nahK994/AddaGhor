import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-edit-user',
  templateUrl: './edit-user.component.html',
  styleUrls: ['./edit-user.component.scss']
})
export class EditUserComponent implements OnInit {

  userId: number;
  formGroup: FormGroup;

  constructor(
    private _activateRoute: ActivatedRoute,
    private _userService: UserService,
    private _router: Router,
    private _fb: FormBuilder
  ) {
    this.formGroup = this._fb.group({
      userName: [''],
      bio: [''],
      occupation: [''],
      email: [''],
      password: ['']
    })
  }

  async ngOnInit(): Promise<void> {
    this.userId = this._activateRoute.snapshot.params['userId'];
    let res = await this._userService.getUser(this.userId);
    this.formGroup.get('userName').setValue(res.userName);
    this.formGroup.get('bio').setValue(res.bio);
    this.formGroup.get('occupation').setValue(res.occupation);
    this.formGroup.get('email').setValue(res.email);
    this.formGroup.get('password').setValue(res.password);
  }

  goToHome() {
    this._router.navigate(['home', this.userId])
  }

  submit() {
    try {
      this._userService.updateUser(this.userId, this.formGroup.value)
      this._router.navigate(['..'], {
        relativeTo: this._activateRoute
      })
    }
    catch(error) {
      console.log(error)
    }
  }

}
