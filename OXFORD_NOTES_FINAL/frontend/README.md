# Oxford LMS - Frontend

HTML/CSS/JavaScript frontend for Oxford LMS.

## Structure

```
frontend/
├── static/                # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   ├── dashboard.js  # Dashboard logic
│   │   ├── login.js      # Login page logic
│   │   └── notes_viewer.js # Document viewer
│   └── assets/
│       └── oxford_logo.jpg # Logo image
├── templates/             # HTML templates
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   └── dashboard.html    # Main dashboard
└── assets/               # Additional assets
```

## Features

### Landing Page (`index.html`)
- Professional landing page with gradient background
- Features grid showcasing LMS capabilities
- Statistics section
- Responsive design

### Login Page (`login.html`)
- Dual-mode authentication (Admin/Student)
- Password visibility toggle
- Modern UI with brand colors
- Session management

### Dashboard (`dashboard.html`)
- Dynamic sidebar navigation
- Role-based content
- Real-time notifications
- Search functionality
- Profile management
- Module switching (Students, Courses, Batches, Attendance, Fees, Notes, Reports)

## Design System

### Colors
- **Primary:** `#1e3a5f` (Navy Blue)
- **Secondary:** `#2563eb` (Blue)
- **Accent:** `#f59e0b` (Amber)
- **Sidebar:** `#0f2340` (Dark Navy)

### Typography
- **Font Family:** Inter, system fonts
- **Headings:** 700-800 weight
- **Body:** 400-500 weight

### Components
- Cards with subtle shadows
- Rounded corners (8px standard)
- Smooth transitions (0.2s)
- Icon buttons
- Form controls
- Modal overlays

## JavaScript Modules

### `dashboard.js`
- Navigation handling
- Module loading
- API communication
- User session management
- CRUD operations for all entities
- Real-time updates

### `notes_viewer.js`
- PDF rendering (PDF.js)
- Video playback
- Document preview
- Download controls
- Watermarking for view-only content

### `login.js`
- Form validation
- Role switching
- Authentication
- Error handling

## API Integration

All frontend JavaScript communicates with backend via:

```javascript
// Base URL
const API_BASE = '/api';

// Example: Fetch students
fetch(`${API_BASE}/students/`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## Development

No build process required. The frontend is served directly by Flask.

To modify:
1. Edit HTML files in `templates/`
2. Edit CSS in `static/css/`
3. Edit JavaScript in `static/js/`
4. Refresh browser to see changes

## Responsive Design

- Mobile-first approach
- Breakpoint: 768px for mobile
- Collapsible sidebar on mobile
- Touch-friendly buttons

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Assets

### Logo
- Location: `static/assets/oxford_logo.jpg`
- Used in: Login, Dashboard sidebar, Document viewer
- Format: JPG with white background

### Icons
- Using inline SVG icons
- Stroke-based design
- 16-24px standard sizes

## Customization

### Change Logo
Replace `static/assets/oxford_logo.jpg` with your logo

### Change Colors
Edit CSS variables in `static/css/style.css`:
```css
:root {
  --brand-primary:   #1e3a5f;
  --brand-secondary: #2563eb;
  --brand-accent:    #f59e0b;
}
```

### Change Branding
Edit text in HTML templates:
- `templates/index.html` - Landing page content
- `templates/login.html` - Login page branding
- `templates/dashboard.html` - Dashboard branding
