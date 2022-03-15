import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from 'src/login-registration-sectioin/login/login.component';

const routes: Routes = [
  {
    path: "",
    redirectTo: "/login",
    pathMatch: 'full'
  },
  {
    path: "login",
    loadChildren: () => import('../login-registration-sectioin/login-registration-sectioin.module').then(m => m.LoginRegistrationSectioinModule)
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
