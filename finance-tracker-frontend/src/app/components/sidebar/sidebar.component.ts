import { Component, ViewChild } from '@angular/core';
import { RouterModule } from '@angular/router';

import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { NgClass, NgIf } from '@angular/common';
import { MatSidenav } from '@angular/material/sidenav';
@Component({
  selector: 'app-sidebar',
  imports: [
    RouterModule,
    MatListModule,
    MatSidenavModule,
    MatIconModule,
    MatToolbarModule,
    MatButtonModule,
    NgClass,
    NgIf,
  ],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css',
})
export class SidebarComponent {
  isCollapsed: boolean = true;
  @ViewChild(MatSidenav)
  sidenav!: MatSidenav;
  toggleMenu() {
    this.sidenav.open();
    this.isCollapsed = !this.isCollapsed;
  }
}
