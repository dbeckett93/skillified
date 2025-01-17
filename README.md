### Overview

Skillified is a community skill-sharing platform designed to connect individuals eager to learn and share skills. Whether it's professional expertise, personal hobbies, or unique talents, Skillified provides a collaborative environment to foster growth and exchange knowledge. The platform addresses the need for accessible, inclusive, and user-friendly learning opportunities while showcasing the potential of modern full-stack web development.

### UX Design Process

### User Stories
- As a user, I want to be able to create an account so that I can access the platform's features.
- As a user, I want to be able to log in and log out so that my account is secure.
- As a user, I want to be able to create and edit my profile so that I can share information about myself.
- As a user, I want to be able to browse and search for skills so that I can find skills I am interested in.
- As a user, I want to be able to join events related to skills I am interested in so that I can learn and share knowledge.
- As a user, I want to be able to create and manage events so that I can share my skills with others.
- As a user, I want to be able to connect with other users so that I can build a network of skill sharers.

For more details, visit the [project page](https://github.com/users/dbeckett93/projects/9/views/1).

### Wireframes

### Main Site Pages
<img src="assets/images/readme/Mobile - Site Pages.png" alt="Main Site Pages Wireframe">

### User Pages
<img src="assets/images/readme/Mobile - User Pages.png" alt="User Pages Wireframe">

### Skills & Events
<img src="assets/images/readme/Mobile - Skills & Events.png" alt="Skills & Events Wireframe">

### ERD

### User

| Field      | Type                   | Relationship                |
|------------|------------------------|-----------------------------|
| id         | Integer (Primary Key)  |                             |
| username   | CharField              |                             |
| email      | EmailField             |                             |
| password   | CharField              |                             |
| first_name | CharField              |                             |
| last_name  | CharField              |                             |
| profile    | OneToOneField          | Profile (One-to-One)        |
| events     | ManyToManyField        | Event (Many-to-Many)        |

### Profile

| Field           | Type                  | Relationship                |
|-----------------|-----------------------|-----------------------------|
| id              | Integer (Primary Key) |                             |
| user            | OneToOneField         | User (One-to-One)           |
| profile_picture | ImageField            |                             |
| about_me        | TextField             |                             |
| facebook_link   | URLField              |                             |
| linkedin_link   | URLField              |                             |
| skills          | ManyToManyField       | Skill (Many-to-Many)        |
| is_mentor  | Boolean                |                             |


### Skill

| Field       | Type                   | Relationship                |
|-------------|------------------------|-----------------------------|
| id          | Integer (Primary Key)  |                             |
| name        | CharField              |                             |
| description | TextField              |                             |
| created_at  | DateTimeField          |                             |
| updated_at  | DateTimeField          |                             |
| profiles    | ManyToManyField        | Profile (Many-to-Many)      |
| events      | ForeignKey             | Event (One-to-Many)         |

### Event

| Field        | Type                   | Relationship                |
|--------------|------------------------|-----------------------------|
| id           | Integer (Primary Key)  |                             |
| title        | CharField              |                             |
| overview     | TextField              |                             |
| date_time    | DateTimeField          |                             |
| skill        | ForeignKey             | Skill (Many-to-One)         |
| participants | ManyToManyField        | User (Many-to-Many)         |

### Message

| Field     | Type                   | Relationship                |
|-----------|------------------------|-----------------------------|
| id        | Integer (Primary Key)  |                             |
| sender    | ForeignKey             | User (Many-to-One)          |
| receiver  | ForeignKey             | User (Many-to-One)          |
| content   | TextField              |                             |
| timestamp | DateTimeField          |                             |

### NotificationSetting

| Field       | Type                   | Relationship                |
|-------------|------------------------|-----------------------------|
| id          | Integer (Primary Key)  |                             |
| user        | ForeignKey             | User (Many-to-One)          |
| new_message | Boolean                |                             |
| new_event   | Boolean                |                             |
| new_skill   | Boolean                |                             |

### Relationships Summary
- User has a one-to-one relationship with Profile.
- User has a many-to-many relationship with Event (as participants).
- Profile has a many-to-many relationship with Skill.
- Skill has a one-to-many relationship with Event.
- Event has a many-to-many relationship with User (as participants).
- Message has a many-to-one relationship with User (as sender and receiver).
- NotificationSetting has a many-to-one relationship with User.