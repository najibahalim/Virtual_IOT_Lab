import { Component, OnInit} from '@angular/core';
import { DragulaService } from 'ng2-dragula';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'dashboardapp';

  constructor(private dragulaService: DragulaService) {
    dragulaService.createGroup('COPYABLE', {
      copy: (el, source) => {
        return source.id === 'left';
      },
      accepts: (el, target, source, sibling) => {
        // To avoid dragging from right to left container
        return target.id !== 'left';
      }
    });

    dragulaService.createGroup('HANDLES', {
      moves: (el, container, handle) => {
        return handle.className === 'handle';
      }
    });
  }
  inBounds = true;
  edge = {
    top: true,
    bottom: true,
    left: true,
    right: true
  };
  ngOnInit() {
  }
  checkEdge(event) {
    this.edge = event;
    console.log('edge:', event);
  }
}
