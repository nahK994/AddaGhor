import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DialogBoxComponent } from './dialog-box/dialog-box.component';

export interface EditedTextOutputFormat {
  itemId: number,
  text: string
}

@Component({
  selector: 'edit-item',
  templateUrl: './edit-item.component.html',
  styleUrls: ['./edit-item.component.scss']
})
export class EditItemComponent implements OnInit {

  @Input() itemId: number = 0;
  @Input() text: string = '';
  @Output() editedText: EventEmitter<EditedTextOutputFormat> = new EventEmitter<EditedTextOutputFormat>();

  constructor(
    public _dialog: MatDialog
  ) { }

  ngOnInit(): void {
  }

  openDialog() {
    const dialogRef = this._dialog.open(DialogBoxComponent, {
      width: '30%',
      minWidth: '400px',
      height: '50%',
      minHeight: '400px',
      data: {
        "text": this.text
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      this.editedText.emit({
        "itemId": this.itemId,
        "text": result
      })
    });
  }

}
