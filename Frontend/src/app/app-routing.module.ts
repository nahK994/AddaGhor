import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
  {
    path: "",
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadChildren: () => import('./login-registration-section/login-registration-section.module').then(m => m.LoginRegistrationSectionModule)
  },
  {
    path: 'home',
    loadChildren: () => import('./home-section/home-section.module').then(m => m.HomeSectionModule)
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
