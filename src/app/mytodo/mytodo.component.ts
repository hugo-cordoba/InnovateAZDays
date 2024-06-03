import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TodoService } from './todo.service';
import { Todo } from './todo.model';

@Component({
  selector: 'app-mytodo',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './mytodo.component.html',
  styleUrls: ['./mytodo.component.css']
})
export class MyTodoComponent implements OnInit {
  todos: Todo[] = [];
  newTodo: Todo = { id: '', name: '', description: '', done: false };

  constructor(private todoService: TodoService) {}

  ngOnInit(): void {
    this.getTodos();
  }

  getTodos(): void {
    this.todoService.getTodos().subscribe((todos) => (this.todos = todos));
  }

  addTodo(): void {
    if (this.newTodo.name && this.newTodo.description) {
      this.todoService.addTodo(this.newTodo).subscribe((todo) => {
        this.todos.push(todo);
        this.newTodo = { id: '', name: '', description: '', done: false };
      });
    }
  }

  deleteTodo(id: string): void {
    this.todoService.deleteTodo(id).subscribe(() => {
      this.todos = this.todos.filter((todo) => todo.id !== id);
    });
  }

  toggleDone(todo: Todo): void {
    todo.done = !todo.done;
    this.todoService.updateTodo(todo.id, todo).subscribe();
  }
}
