import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyeventComponent } from './myevent.component';

describe('MyeventComponent', () => {
  let component: MyeventComponent;
  let fixture: ComponentFixture<MyeventComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyeventComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MyeventComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
