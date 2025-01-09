### Overview

Skillified is a community skill-sharing platform designed to connect individuals eager to learn and share skills. Whether it's professional expertise, personal hobbies, or unique talents, Skillified provides a collaborative environment to foster growth and exchange knowledge. The platform addresses the need for accessible, inclusive, and user-friendly learning opportunities while showcasing the potential of modern full-stack web development.

### UX Design Process
//Project link user stories//

### Wireframes

![Homepage Wireframe](assets/images/readme/homepage_wireframe.png)
![Profile Page Wireframe](assets/images/readme/profile_page_wireframe.png)
![Skill Sharing Page Wireframe](assets/images/readme/skill_sharing_page_wireframe.png)

### ERD

### User

| Field      | Type                | Relationship            |
|------------|---------------------|-------------------------|
| id         | Integer (Primary Key) |                         |
| username   | CharField           |                         |
| email      | EmailField          |                         |
| password   | CharField           |                         |
| first_name | CharField           |                         |
| last_name  | CharField           |                         |
| profile    | OneToOneField       | Profile (One-to-One)    |
| events     | ManyToManyField     | Event (Many-to-Many)    |

### Profile

| Field           | Type                | Relationship            |
|-----------------|---------------------|-------------------------|
| id              | Integer (Primary Key) |                         |
| user            | OneToOneField       | User (One-to-One)       |
| profile_picture | ImageField          |                         |
| about_me        | TextField           |                         |
| facebook_link   | URLField            |                         |
| linkedin_link   | URLField            |                         |
| skills          | ManyToManyField     | Skill (Many-to-Many)    |

### Skill

| Field       | Type                | Relationship            |
|-------------|---------------------|-------------------------|
| id          | Integer (Primary Key) |                         |
| name        | CharField           |                         |
| description | TextField           |                         |
| created_at  | DateTimeField       |                         |
| updated_at  | DateTimeField       |                         |
| users       | ManyToManyField     | Profile (Many-to-Many)  |
| events      | ForeignKey          | Event (One-to-Many)     |

### Event

| Field        | Type                | Relationship            |
|--------------|---------------------|-------------------------|
| id           | Integer (Primary Key) |                         |
| title        | CharField           |                         |
| overview     | TextField           |                         |
| date_time    | DateTimeField       |                         |
| skill        | ForeignKey          | Skill (Many-to-One)     |
| participants | ManyToManyField     | User (Many-to-Many)     |

### Relationships Summary
User has a one-to-one relationship with Profile.
User has a many-to-many relationship with Event (as participants).
Profile has a many-to-many relationship with Skill.
Skill has a one-to-many relationship with Event.
Event has a many-to-many relationship with User (as participants).