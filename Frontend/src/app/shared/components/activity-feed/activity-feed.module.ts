import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivityFeedComponent } from './activity-feed.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';
import {MatCardModule} from '@angular/material/card';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import { ActivityFeedService } from './activity-feed.service';
import { HttpClientModule } from '@angular/common/http';
import { EditItemModule } from '../edit-item/edit-item.module';

@NgModule({
  declarations: [ActivityFeedComponent],
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    HttpClientModule,
    EditItemModule
  ],
  exports: [
    ActivityFeedComponent
  ],
  providers: [
    ActivityFeedService
  ]
})
export class ActivityFeedModule { }
