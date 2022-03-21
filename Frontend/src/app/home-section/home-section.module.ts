import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { HomeSectoinRoutingModule } from './home-section-routing-module';



@NgModule({
  declarations: [LandingPageComponent],
  imports: [
    CommonModule,
    HomeSectoinRoutingModule
  ]
})
export class HomeSectionModule { }
