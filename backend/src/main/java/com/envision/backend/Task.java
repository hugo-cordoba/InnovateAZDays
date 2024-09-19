package com.envision.backend;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Task {
    @Id
    private String id;
    private String name;
    private String description;
    private boolean done;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public boolean isDone() {
        return done;
    }

    public void setDone(boolean done) {
        this.done = done;
    }

    // Getters y setters

}