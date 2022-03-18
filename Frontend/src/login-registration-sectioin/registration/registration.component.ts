import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

  constructor(
    private dialogRef: MatDialogRef<RegistrationComponent>
  ) { }

  ngOnInit(): void {
  }

  closeWindow() {
    this.dialogRef.close();
    console.log("hi");
  }

}
