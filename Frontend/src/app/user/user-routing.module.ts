import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateUserComponent } from './create-user/create-user.component';
import { EditUserComponent } from './edit-user/edit-user.component';
import { ActivateUserComponent } from './activate-user/activate-user.component';

const routes: Routes = [
  {
    path: 'create',
    component: CreateUserComponent
  },
  {
    path: 'user-profile/:userId',
    component: EditUserComponent
  },
  {
    path: ':userId/activate/:code',
    component: ActivateUserComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
