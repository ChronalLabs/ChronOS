# CIVISIM Authentication Setup

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google+ API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure OAuth consent screen
6. Create **Web application** credentials
7. Add authorized JavaScript origins:
   - `http://localhost:3000`
   - `http://localhost:3001`
   - Your production URL
8. Copy the **Client ID** and add to `.env` as `VITE_GOOGLE_CLIENT_ID`

## Admin Configuration

Edit `frontend/src/context/AuthContext.tsx` and add admin emails to `ADMIN_EMAILS` array:

```typescript
const ADMIN_EMAILS = [
  'admin@civisim.com',
  'your-admin-email@gmail.com',
  'another-admin@example.com'
]
```

## User Roles

### Admin Role
- Full access to all features
- Can create, edit, and delete
- Access to ML Analysis
- Access to Simulation Engine
- Access to Policy Configuration

### Public Role
- View-only access
- Can view Impact Analysis
- Can view Impact Map
- Cannot modify data

## Testing

1. Login with admin email → Gets Admin role
2. Login with other email → Gets Public role
3. Try accessing admin routes as public user → Access Denied
