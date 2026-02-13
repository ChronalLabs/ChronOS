package com.rtigen.model;

import org.springframework.data.annotation.Id;
import java.util.List;

public class Template {
    @Id
    private String id;
    private String title;
    private String department;
    private String state;
    private List<String> tags;
    private String subject;
    private List<String> questions;
    private String content;
    private int usageCount = 0;

    public Template() {
    }

    public Template(String id, String title, String department, String state, List<String> tags, String subject,
            List<String> questions, String content, int usageCount) {
        this.id = id;
        this.title = title;
        this.department = department;
        this.state = state;
        this.tags = tags;
        this.subject = subject;
        this.questions = questions;
        this.content = content;
        this.usageCount = usageCount;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public List<String> getTags() {
        return tags;
    }

    public void setTags(List<String> tags) {
        this.tags = tags;
    }

    public String getSubject() {
        return subject;
    }

    public void setSubject(String subject) {
        this.subject = subject;
    }

    public List<String> getQuestions() {
        return questions;
    }

    public void setQuestions(List<String> questions) {
        this.questions = questions;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public int getUsageCount() {
        return usageCount;
    }

    public void setUsageCount(int usageCount) {
        this.usageCount = usageCount;
    }
}
