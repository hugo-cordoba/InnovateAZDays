import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TodoListService } from './todolist.service';
import { Task } from './todolist.model';

@Component({
  selector: 'app-todolist',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './todolist.component.html',
  styleUrls: ['./todolist.component.css']
})
export class TodoListComponent {
  tasks: Task[] = [];
  newTask: Task = { id: '', name: '', description: '', done: false };

  constructor(private todoListService: TodoListService) {
    this.loadTasks();
  }

  loadTasks(): void {
    this.todoListService.getTasks().subscribe((tasks) => (this.tasks = tasks));
  }

  addTask(): void {
    if (this.newTask.name && this.newTask.description) {
      this.todoListService.addTask(this.newTask).subscribe((task) => {
        this.tasks.push(task);
        this.newTask = { id: '', name: '', description: '', done: false };
      });
    }
  }

  updateTask(task: Task): void {
    this.todoListService.updateTask(task).subscribe();
  }

  deleteTask(id: string): void {
    this.todoListService.deleteTask(id).subscribe(() => {
      this.tasks = this.tasks.filter((task) => task.id !== id);
    });
  }
}
