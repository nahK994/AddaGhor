import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlaygroundComponent } from './playground.component';
import { ShomiComponent } from './shomi/shomi.component';
import { SabbirComponent } from './sabbir/sabbir.component';
import { PlaygroundRoutingModule } from './playground-routing.module';
import { UserModule } from '../user/user.module';
import { HomeModule } from '../home/home.module';

@NgModule({
  declarations: [PlaygroundComponent, ShomiComponent, SabbirComponent],
  imports: [
    CommonModule,
    PlaygroundRoutingModule,
    UserModule,
    HomeModule
  ]
})
export class PlaygroundModule { }