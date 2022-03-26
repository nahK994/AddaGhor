import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { PostComponent } from 'src/app/shared/post/post.component';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {

  constructor(
    public dialog: MatDialog
  ) { }

  ngOnInit(): void {
  }

  openCreatePostDialogue() {
    const dialogRef = this.dialog.open(PostComponent, {
      width: '520px',
      height: '380px'
    });

    dialogRef.afterClosed().subscribe(result => {
      ///Call Api Using this result data to create new account
      console.log(result.value);
    });
  }

}
