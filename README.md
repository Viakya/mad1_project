# 🎵 Music Streaming Platform - My First Ever Project

> **A Special Note**: This was my first-ever programming project! While it may not be perfect, it represents the start of an incredible learning journey. Every bug fixed, every feature added, and every line of code written here taught me something valuable about software development.

## 📖 Project Overview

This is a **Flask-based music streaming platform** - the very first project marking the beginning of my development journey. Built as a Modern Application Development I (MAD1) course project, it demonstrates fundamental web development concepts including user authentication, CRUD operations, and role-based access control.

A multi-user music streaming platform where users can discover music, creators can upload their songs, and admins can moderate the platform - all built from scratch as my introduction to web development!

## 💡 Project Concept

A multi-user music streaming platform with three distinct user roles:

- **🎧 General Users**: Listen to music, create playlists, like songs
- **🎤 Creators**: Upload and manage their own music and albums  
- **👑 Admin**: Moderate content, manage users, handle flagged content

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite3
- **Frontend**: HTML templates with Jinja2
- **Styling**: CSS (in static folder)
- **Architecture**: Traditional server-side rendered MVC pattern

## 🗄️ Database Schema

### Core Models

Based on the `music.py` file, the application uses the following database models:

1. **User** - User accounts (credentials, email, name)
2. **User_Type** - User role definitions (general, creator, admin)
3. **Song** - Music track information (title, artist, file path, duration)
4. **Album** - Album collections
5. **Playlist** - User-created playlists
6. **Like_Song** - User song likes/favorites
7. **Album_Song** - Many-to-many relationship between albums and songs
8. **Playlist_Song** - Many-to-many relationship between playlists and songs
9. **Black_Song** - Flagged/blocked songs
10. **Black_Album** - Flagged/blocked albums  
11. **Black_Creator** - Flagged/blocked creator accounts

## ✨ Key Features

### For General Users
- ✅ User registration and login
- ✅ Browse songs and albums
- ✅ Search functionality for songs, albums, and artists
- ✅ Play music tracks
- ✅ Like/unlike songs
- ✅ Create and manage personal playlists
- ✅ Add songs to playlists
- ✅ View liked songs collection

### For Creators
- ✅ All general user features
- ✅ Upload new songs with metadata
- ✅ Create and manage albums
- ✅ Add songs to albums
- ✅ Update song information
- ✅ View upload history
- ✅ Creator dashboard

### For Admins
- ✅ View all users, songs, albums, playlists
- ✅ Moderate content (flag/block inappropriate content)
- ✅ Block problematic creators
- ✅ Remove flagged songs and albums
- ✅ User management
- ✅ Platform-wide statistics dashboard

## 📁 File Structure

```
mad1_project/
├── music.py                    # Main Flask application with routes and models
├── listen_music.sqlite3        # SQLite database file
├── templates/                  # HTML templates (44 files)
│   ├── start.html             # Landing page
│   ├── register_new.html      # User registration
│   ├── user_login.html        # User login
│   ├── admin_login.html       # Admin login
│   ├── home_tem.html          # User home page
│   ├── creator_tem.html       # Creator dashboard
│   ├── admin_tem.html         # Admin dashboard
│   ├── playing_song.html      # Music player
│   ├── search_tem.html        # Search interface
│   ├── liked_song.html        # Liked songs page
│   ├── view_playlist.html     # Playlist view
│   ├── create_new_playlist.html
│   ├── creator_upload_song.html
│   ├── creating_new_album.html
│   ├── album_detail.html
│   ├── admin_user.html        # Admin user management
│   ├── admin_song.html        # Admin song management
│   ├── admin_album.html       # Admin album management
│   └── [many more templates]
└── static/                     # CSS, JS, and assets
    └── song_20/               # Uploaded music files
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/Viakya/mad1_project.git
cd mad1_project

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-sqlalchemy

# Run the application
python music.py
```

### Access the Application
- Open browser and navigate to: `http://localhost:5000`
- Default port may vary based on Flask configuration

## 👥 User Workflows

### As a New User
1. Visit landing page (`start.html`)
2. Register new account (`register_new.html`)
3. Login with credentials (`user_login.html`)
4. Browse music library (`home_tem.html`)
5. Search for songs/albums (`search_tem.html`)
6. Play songs (`playing_song.html`)
7. Like favorite songs
8. Create playlists (`create_new_playlist.html`)

### As a Creator
1. Register as creator during signup
2. Access creator dashboard (`creator_tem.html`)
3. Upload songs (`creator_upload_song.html`)
4. Create albums (`creating_new_album.html`)
5. Manage uploaded content (`creator_update_song.html`)
6. Add songs to albums

### As an Admin
1. Login with admin credentials (`admin_login.html`)
2. View dashboard (`admin_tem.html`)
3. Monitor all platform activity
4. Review flagged content
5. Block inappropriate users/songs/albums
6. Manage user accounts

## 📄 Template Files (44 Total)

The project includes extensive HTML templates for every feature:

**Authentication & Onboarding:**
- `start.html`, `register_new.html`, `user_login.html`, `admin_login.html`

**User Interface:**
- `home_tem.html`, `you_tem.html`, `about_you.html`, `search_tem.html`

**Music Playback:**
- `playing_song.html`, `play_block_song.html`, `liked_song.html`

**Playlists:**
- `view_playlist.html`, `create_new_playlist.html`, `update_playlist.html`, `add_song_to_playlist.html`

**Albums:**
- `album_detail.html`, `home_album_detail.html`, `album_on_search.html`, `creating_new_album.html`, `update_album.html`, `add_song_to_album.html`, `home_album_block.html`

**Creator Features:**
- `creator_tem.html`, `real_creator_tem.html`, `creator_upload_song.html`, `creator_update_song.html`, `creator_block.html`

**Admin Features:**
- `admin_tem.html`, `admin_user.html`, `admin_song.html`, `admin_album.html`, `admin_playlist.html`, `admin_like_song.html`, `admin_usertype.html`, `admin_album_song.html`, `admin_playlist_song.html`

**Notifications:**
- `notice_after_registration.html`, `notice_song_uploaded_done.html`, `notice_email_already_exists.html`, `notice_wrong_login_details.html`, `notice_after_adding_album.html`, `notice_album_song.html`, `error_not_solved.html`

**Search Results:**
- `song_on_search.html`, `album_on_search.html`

[View all templates in the repository](https://github.com/Viakya/mad1_project/tree/master/templates)

## 📚 What I Learned Building This

### Technical Skills
- Flask framework fundamentals
- SQLAlchemy ORM and database relationships
- User authentication and session management
- CRUD operations (Create, Read, Update, Delete)
- Jinja2 templating engine
- Role-based access control
- HTML/CSS basics
- File handling for music uploads
- Search functionality implementation

### Software Development Concepts
- MVC (Model-View-Controller) architecture
- Database schema design
- Many-to-many relationships
- User roles and permissions
- Content moderation systems
- RESTful route design

### Soft Skills
- Breaking down complex features into manageable tasks
- Debugging and problem-solving
- Planning database structure
- User experience thinking
- Iterative development

## 🎯 Challenges Faced

As a first project, this came with many learning moments:
- Understanding Flask routing and request handling
- Managing database relationships properly
- Implementing authentication without security vulnerabilities
- Handling file uploads for music
- Creating a consistent user interface across 44 templates
- Debugging database query issues
- Managing user sessions

## 🔧 Areas for Improvement

Looking back as a more experienced developer:
- Could add password hashing for security
- API could be RESTful instead of server-side rendered
- Frontend could use JavaScript frameworks
- Database could use migrations (Flask-Migrate)
- Could add automated tests
- Error handling could be more robust
- Could implement proper music file storage (cloud storage)
- CSS could be more maintainable (use preprocessor)
- Could add email verification
- Could implement streaming protocol for music

## 🚀 Future Enhancements (If Continued)

- User profile customization
- Social features (follow creators, share playlists)
- Music recommendations algorithm
- Advanced search with filters
- Audio visualization
- Mobile-responsive design
- RESTful API for mobile apps
- Comment system on songs/albums
- Creator analytics dashboard
- Payment integration for premium features

## 🧪 Running Tests

No automated tests were implemented (a learning for future projects!)

## 🤝 Contributing

This is a learning project and is complete as-is. However, feel free to fork and experiment!

## 📜 License

No license specified (educational project)

## 🙏 Acknowledgments

- Built as part of Modern Application Development I (MAD1) course
- Thanks to all the Stack Overflow answers that helped debug issues!
- Appreciation for Flask documentation and tutorials
- Gratitude to everyone who supported me during my first coding project

## 💭 Reflection

This project holds a special place as the **very first application I ever built**. It's not perfect, and I can now see countless ways to improve it, but it represents the beginning of my journey as a developer. 

Every developer has a "first project" - this is mine. Looking at this code now reminds me how far I've come, and how much there still is to learn. If you're building your first project right now, keep going! The bugs, the errors, the late nights debugging - they're all part of the journey.

> **"Every expert was once a beginner. Every master was once a disaster."**

This project taught me that code doesn't have to be perfect to be valuable. It just has to work, teach you something, and move you forward.

---

**Project Status:** ✅ Complete (Educational milestone)  
**Created:** 2024  
**Repository:** [Viakya/mad1_project](https://github.com/Viakya/mad1_project)

*Built with ❤️ and a lot of coffee as my first-ever coding project*
