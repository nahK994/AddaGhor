import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateUserComponent } from './create-user/create-user.component';
import { EditUserComponent } from './edit-user/edit-user.component';
import { ProfileComponent } from './profile/profile.component';

const routes: Routes = [
  {
    path: 'create',
    component: CreateUserComponent
  },
  {
    path: 'user-profile/:userId/edit',
    component: EditUserComponent
  },
  {
    path: 'user-profile/:userId',
    component: ProfileComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
