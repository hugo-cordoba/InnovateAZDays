import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TodolistmanagerComponent } from './todolistmanager.component';

describe('TodolistmanagerComponent', () => {
  let component: TodolistmanagerComponent;
  let fixture: ComponentFixture<TodolistmanagerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TodolistmanagerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TodolistmanagerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
