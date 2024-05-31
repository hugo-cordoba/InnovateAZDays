import { Component, OnInit } from '@angular/core';
import { Todo } from './todo.model';
import { TodoService } from './todo.service';

@Component({
  selector: 'app-todolistmanager',
  templateUrl: './todolistmanager.component.html',
  styleUrls: ['./todolistmanager.component.css']
})
export class TodolistmanagerComponent implements OnInit {
  todos: Todo[] = [];
  newTodo: Todo = { id: '', name: '', description: '', done: false };

  constructor(private todoService: TodoService) {}

  ngOnInit(): void {
    this.loadTodos();
  }

  loadTodos(): void {
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

  updateTodo(todo: Todo): void {
    this.todoService.updateTodo(todo).subscribe();
  }

  deleteTodo(id: string): void {
    this.todoService.deleteTodo(id).subscribe(() => {
      this.todos = this.todos.filter((todo) => todo.id !== id);
    });
  }
}
