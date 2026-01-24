# Authentication Pages - UI/UX Specification

**Version**: 1.0.0  
**Last Updated**: January 24, 2026

## Overview

This document specifies the UI/UX design for all authentication-related pages: Login, Registration, Password Reset, and Email Verification. These pages are the first touchpoint for users and must balance security with simplicity.

---

## 1. Login Page

**Route**: `/login`  
**Access**: Public only (redirect to `/dashboard` if authenticated)

### 1.1 Layout

```
┌─────────────────────────────────────────────┐
│  [Logo]                                      │
│                                              │
│  ┌─────────────────────────────────────┐   │
│  │  Welcome Back                        │   │
│  │                                      │   │
│  │  [Email input field]                 │   │
│  │  [Password input field]              │   │
│  │                                      │   │
│  │  ☐ Remember me    [Forgot password?]│   │
│  │                                      │   │
│  │  [Login Button - Full width]        │   │
│  │                                      │   │
│  │  ────── or ──────                    │   │
│  │                                      │   │
│  │  [Continue with Google] (future)    │   │
│  │                                      │   │
│  │  Don't have an account? [Sign up]   │   │
│  └─────────────────────────────────────┘   │
│                                              │
└─────────────────────────────────────────────┘
```

### 1.2 Components

**Email Input**:
```html
<div class="form-group">
  <label for="email">Email Address</label>
  <input 
    type="email" 
    id="email"
    placeholder="you@example.com"
    required
    autocomplete="email"
  />
  <span class="error-message" hidden>Please enter a valid email</span>
</div>
```

**Password Input**:
```html
<div class="form-group">
  <label for="password">Password</label>
  <div class="password-input-wrapper">
    <input 
      type="password" 
      id="password"
      placeholder="Enter your password"
      required
      autocomplete="current-password"
    />
    <button type="button" class="toggle-password" aria-label="Show password">
      [👁️ icon]
    </button>
  </div>
  <span class="error-message" hidden>Password is required</span>
</div>
```

**Remember Me Checkbox**:
```html
<label class="checkbox-label">
  <input type="checkbox" id="remember" />
  <span>Remember me for 30 days</span>
</label>
```

**Login Button**:
```html
<button type="submit" class="btn btn-primary btn-block">
  <span>Log In</span>
  <span class="spinner" hidden></span>
</button>
```

### 1.3 States

**Default State**:
- All fields empty
- Submit button enabled
- No error messages

**Validation States**:
- **Invalid Email**: Red border on email input, error message below
- **Empty Password**: Red border on password input, error message below
- **Invalid Credentials**: Global error message above form

**Loading State**:
- Submit button disabled
- Button text changes to "Logging in..."
- Spinner appears in button
- All inputs disabled

**Success State**:
- Brief success message: "Welcome back!"
- Redirect to dashboard (200ms delay for UX)

**Error States**:
| Error | Message | Action |
|-------|---------|--------|
| Invalid email format | "Please enter a valid email address" | Focus email field |
| Empty password | "Password is required" | Focus password field |
| Wrong credentials | "Invalid email or password" | Clear password, focus email |
| Account not verified | "Please verify your email first. [Resend email]" | Show link |
| Too many attempts | "Too many login attempts. Please try again in 5 minutes." | Disable form |
| Network error | "Connection error. Please check your internet and try again." | Show retry |

### 1.4 Interactions

**Form Submission Flow**:
1. User fills email and password
2. User clicks "Log In" or presses Enter
3. Client-side validation runs
4. If valid, show loading state
5. Send POST request to `/api/v1/auth/login`
6. On success: Store JWT, redirect to dashboard
7. On error: Show error message, reset form

**"Show Password" Toggle**:
- Click toggles between `type="password"` and `type="text"`
- Icon changes between closed eye and open eye
- Tooltip: "Show password" / "Hide password"

**"Remember Me" Checkbox**:
- If checked: Set longer JWT expiry (30 days)
- If unchecked: Session expires when browser closes
- Default: Unchecked

### 1.5 Responsive Design

**Desktop (≥768px)**:
- Form centered horizontally
- Max width: 400px
- Vertical padding: 80px

**Mobile (<768px)**:
- Full width form (with 16px padding)
- Larger touch targets (48px min)
- Keyboard pushes form up (use `position: fixed` header)

### 1.6 Accessibility

- Proper `<label>` for each input
- ARIA labels on buttons
- Error messages announced by screen readers
- Keyboard navigation: Tab through fields, Enter to submit
- Focus visible styles
- High contrast mode support

### 1.7 API Integration

**Endpoint**: `POST /api/v1/auth/login`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "remember_me": true
}
```

**Success Response (200)**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 2592000,
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "email_verified": true
  }
}
```

**Error Response (401)**:
```json
{
  "detail": "Invalid credentials"
}
```

---

## 2. Registration Page

**Route**: `/register`  
**Access**: Public only

### 2.1 Layout

```
┌─────────────────────────────────────────────┐
│  [Logo]                                      │
│                                              │
│  ┌─────────────────────────────────────┐   │
│  │  Create Your Account                 │   │
│  │                                      │   │
│  │  [Full Name input]                   │   │
│  │  [Email input]                       │   │
│  │  [Password input]                    │   │
│  │  [Confirm Password input]            │   │
│  │                                      │   │
│  │  Password Requirements:              │   │
│  │  ✓ At least 8 characters             │   │
│  │  ✓ One uppercase letter              │   │
│  │  ✓ One number                        │   │
│  │  ✓ One special character             │   │
│  │                                      │   │
│  │  ☐ I agree to Terms & Privacy Policy│   │
│  │                                      │   │
│  │  [Sign Up Button]                    │   │
│  │                                      │   │
│  │  Already have an account? [Log in]   │   │
│  └─────────────────────────────────────┘   │
│                                              │
└─────────────────────────────────────────────┘
```

### 2.2 Components

**Full Name Input**:
```html
<div class="form-group">
  <label for="name">Full Name</label>
  <input 
    type="text" 
    id="name"
    placeholder="John Doe"
    required
    autocomplete="name"
    minlength="2"
    maxlength="100"
  />
  <span class="error-message" hidden>Name must be at least 2 characters</span>
</div>
```

**Password Strength Indicator**:
```html
<div class="password-strength">
  <div class="strength-bar">
    <div class="strength-fill" data-strength="0"></div>
  </div>
  <span class="strength-text">Weak</span>
</div>
```

**Password Requirements Checklist**:
```html
<ul class="password-requirements">
  <li data-met="false">
    <span class="icon">○</span>
    <span>At least 8 characters</span>
  </li>
  <li data-met="false">
    <span class="icon">○</span>
    <span>One uppercase letter</span>
  </li>
  <li data-met="false">
    <span class="icon">○</span>
    <span>One number</span>
  </li>
  <li data-met="false">
    <span class="icon">○</span>
    <span>One special character (!@#$%^&*)</span>
  </li>
</ul>
```

When requirement is met: `data-met="true"`, icon changes to "✓", text color green.

**Terms Agreement Checkbox**:
```html
<label class="checkbox-label">
  <input type="checkbox" id="terms" required />
  <span>
    I agree to the 
    <a href="/terms" target="_blank">Terms of Service</a> and 
    <a href="/privacy" target="_blank">Privacy Policy</a>
  </span>
</label>
```

### 2.3 Validation Rules

**Name**:
- Required
- 2-100 characters
- Only letters, spaces, hyphens, apostrophes
- Pattern: `/^[a-zA-Z\s'-]{2,100}$/`

**Email**:
- Required
- Valid email format
- Not already registered (checked on submit)
- Pattern: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`

**Password**:
- Required
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character
- Pattern: `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/`

**Confirm Password**:
- Must match Password field exactly
- Real-time validation as user types

**Terms Checkbox**:
- Must be checked to submit

### 2.4 States

**Password Strength Levels**:
- **Weak** (0-2 requirements): Red bar (20% width)
- **Fair** (3 requirements): Orange bar (50% width)
- **Strong** (4 requirements): Green bar (100% width)

**Form States**:
- **Pristine**: No validation shown
- **Touched**: Show validation after field blur
- **Submitting**: Loading state, button disabled
- **Success**: "Account created! Redirecting..."
- **Error**: Show error message, focus first invalid field

### 2.5 Interactions

**Real-time Validation**:
- Email format: Check on blur
- Password strength: Check on every keystroke
- Confirm password: Check on every keystroke
- Requirements checklist: Update on every keystroke

**Registration Flow**:
1. User fills all fields
2. All validations pass (green checkmarks)
3. Terms checkbox checked
4. Click "Sign Up"
5. Show loading state
6. Send POST to `/api/v1/auth/register`
7. On success:
   - Show success message
   - Send verification email
   - Redirect to verification prompt page
8. On error:
   - Show error message
   - Keep form filled (don't clear password)

### 2.6 Error Messages

| Error | Message | Action |
|-------|---------|--------|
| Email already exists | "This email is already registered. [Log in instead?]" | Link to login |
| Invalid email | "Please enter a valid email address" | Focus email |
| Weak password | "Password must meet all requirements" | Focus password |
| Passwords don't match | "Passwords do not match" | Focus confirm |
| Terms not accepted | "Please accept the Terms of Service" | Focus checkbox |
| Network error | "Registration failed. Please try again." | Retry button |

### 2.7 API Integration

**Endpoint**: `POST /api/v1/auth/register`

**Request**:
```json
{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Success Response (201)**:
```json
{
  "id": "user_456",
  "email": "newuser@example.com",
  "email_verified": false,
  "created_at": "2026-01-24T10:30:00Z",
  "message": "Registration successful. Please check your email to verify your account."
}
```

**Error Response (400)**:
```json
{
  "detail": "Email already registered"
}
```

---

## 3. Password Reset Page

**Routes**: 
- Request: `/reset-password`
- Reset: `/reset-password/:token`

**Access**: Public only

### 3.1 Request Reset Layout

```
┌─────────────────────────────────────────────┐
│  [Logo]                                      │
│                                              │
│  ┌─────────────────────────────────────┐   │
│  │  Reset Your Password                 │   │
│  │                                      │   │
│  │  Enter your email address and we'll  │   │
│  │  send you a link to reset your       │   │
│  │  password.                           │   │
│  │                                      │   │
│  │  [Email input field]                 │   │
│  │                                      │   │
│  │  [Send Reset Link Button]            │   │
│  │                                      │   │
│  │  [← Back to Login]                   │   │
│  └─────────────────────────────────────┘   │
│                                              │
└─────────────────────────────────────────────┘
```

### 3.2 Components

**Email Input**:
```html
<div class="form-group">
  <label for="email">Email Address</label>
  <input 
    type="email" 
    id="email"
    placeholder="you@example.com"
    required
    autocomplete="email"
  />
</div>
```

**Send Button**:
```html
<button type="submit" class="btn btn-primary btn-block">
  Send Reset Link
</button>
```

### 3.3 States

**Success State** (after submission):
```
┌─────────────────────────────────────┐
│  ✓ Check Your Email                 │
│                                     │
│  If an account exists for           │
│  user@example.com, you will         │
│  receive a password reset link      │
│  shortly.                           │
│                                     │
│  Didn't receive the email?          │
│  [Resend Link]                      │
│                                     │
│  [← Back to Login]                  │
└─────────────────────────────────────┘
```

**Security Note**: Always show success message even if email doesn't exist (to prevent email enumeration attacks).

### 3.4 Reset Password Layout

**Route**: `/reset-password/:token`

```
┌─────────────────────────────────────────────┐
│  [Logo]                                      │
│                                              │
│  ┌─────────────────────────────────────┐   │
│  │  Set New Password                    │   │
│  │                                      │   │
│  │  [New Password input]                │   │
│  │  [Confirm Password input]            │   │
│  │                                      │   │
│  │  Password Requirements:              │   │
│  │  ✓ At least 8 characters             │   │
│  │  ✓ One uppercase letter              │   │
│  │  ✓ One number                        │   │
│  │  ✓ One special character             │   │
│  │                                      │   │
│  │  [Reset Password Button]             │   │
│  └─────────────────────────────────────┘   │
│                                              │
└─────────────────────────────────────────────┘
```

### 3.5 Token Validation

**On Page Load**:
1. Extract token from URL
2. Validate token format (JWT)
3. Check if token expired
4. If invalid: Show error page

**Error Page** (invalid/expired token):
```
┌─────────────────────────────────────┐
│  ⚠️ Invalid or Expired Link          │
│                                     │
│  This password reset link is no     │
│  longer valid. Please request a     │
│  new one.                           │
│                                     │
│  [Request New Link]                 │
└─────────────────────────────────────┘
```

### 3.6 API Integration

**Request Reset Endpoint**: `POST /api/v1/auth/password-reset/request`

**Request**:
```json
{
  "email": "user@example.com"
}
```

**Response (200)** (always, even if email doesn't exist):
```json
{
  "message": "If an account exists, a reset link has been sent"
}
```

**Reset Password Endpoint**: `POST /api/v1/auth/password-reset/confirm`

**Request**:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "new_password": "NewSecurePass123!"
}
```

**Success Response (200)**:
```json
{
  "message": "Password reset successful"
}
```

**Error Response (400)**:
```json
{
  "detail": "Invalid or expired token"
}
```

---

## 4. Email Verification Page

**Route**: `/verify-email/:token`  
**Access**: Public

### 4.1 Verifying State Layout

```
┌─────────────────────────────────────────────┐
│  [Logo]                                      │
│                                              │
│  ┌─────────────────────────────────────┐   │
│  │  [Spinner animation]                 │   │
│  │                                      │   │
│  │  Verifying your email...             │   │
│  └─────────────────────────────────────┘   │
│                                              │
└─────────────────────────────────────────────┘
```

### 4.2 Success State

```
┌─────────────────────────────────────────────┐
│  [Logo]                                      │
│                                              │
│  ┌─────────────────────────────────────┐   │
│  │  ✓ Email Verified!                   │   │
│  │                                      │   │
│  │  Your email has been successfully    │   │
│  │  verified. You can now log in and    │   │
│  │  start using Vuva.                   │   │
│  │                                      │   │
│  │  [Continue to Login]                 │   │
│  └─────────────────────────────────────┘   │
│                                              │
└─────────────────────────────────────────────┘
```

Auto-redirect to login after 3 seconds.

### 4.3 Error States

**Invalid Token**:
```
┌─────────────────────────────────────┐
│  ⚠️ Verification Failed              │
│                                     │
│  This verification link is invalid  │
│  or has expired.                    │
│                                     │
│  [Resend Verification Email]        │
└─────────────────────────────────────┘
```

**Already Verified**:
```
┌─────────────────────────────────────┐
│  ℹ️ Already Verified                 │
│                                     │
│  Your email has already been        │
│  verified. You can log in now.      │
│                                     │
│  [Go to Login]                      │
└─────────────────────────────────────┘
```

### 4.4 API Integration

**Endpoint**: `POST /api/v1/auth/verify-email`

**Request**:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200)**:
```json
{
  "message": "Email verified successfully",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "email_verified": true
  }
}
```

---

## 5. Design Specifications

### 5.1 Typography

**Headings**:
- Page title: 32px, font-weight 700, color: gray-900
- Form title: 24px, font-weight 600, color: gray-900
- Labels: 14px, font-weight 500, color: gray-700

**Body Text**:
- Input text: 16px, font-weight 400, color: gray-900
- Placeholder: 16px, font-weight 400, color: gray-400
- Helper text: 14px, font-weight 400, color: gray-600
- Error text: 14px, font-weight 500, color: red-600

### 5.2 Colors

**Inputs**:
- Border (default): gray-300
- Border (focus): primary-500
- Border (error): red-500
- Background: white
- Text: gray-900

**Buttons**:
- Primary: bg-primary-600, hover:bg-primary-700
- Secondary: bg-gray-200, hover:bg-gray-300
- Text: white (primary), gray-900 (secondary)

**Errors**:
- Background: red-50
- Border: red-200
- Text: red-600
- Icon: red-500

**Success**:
- Background: green-50
- Border: green-200
- Text: green-600
- Icon: green-500

### 5.3 Spacing

- Form max-width: 400px
- Input height: 48px
- Button height: 48px
- Input padding: 12px 16px
- Vertical spacing between fields: 20px
- Vertical spacing sections: 32px

### 5.4 Animations

**Input Focus**:
```css
transition: border-color 200ms ease, box-shadow 200ms ease;
```

**Button Hover**:
```css
transition: background-color 200ms ease, transform 100ms ease;
```

**Button Press**:
```css
transform: scale(0.98);
```

**Error Shake**:
```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}
```

**Loading Spinner**:
```css
@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## 6. User Flows

### 6.1 Registration Flow

```
User visits /register
    ↓
Fills registration form
    ↓
Client-side validation passes
    ↓
Submits form
    ↓
POST /api/v1/auth/register
    ↓
Success: Account created
    ↓
Redirect to verification prompt
    ↓
User checks email
    ↓
Clicks verification link
    ↓
Redirected to /verify-email/:token
    ↓
Email verified
    ↓
Redirect to login
    ↓
User logs in
    ↓
Redirect to dashboard
```

### 6.2 Login Flow

```
User visits /login
    ↓
Enters email and password
    ↓
Clicks "Log In"
    ↓
POST /api/v1/auth/login
    ↓
Success: JWT token received
    ↓
Store token (localStorage/cookie)
    ↓
Update auth state
    ↓
Redirect to dashboard
```

### 6.3 Password Reset Flow

```
User clicks "Forgot password?"
    ↓
Redirected to /reset-password
    ↓
Enters email address
    ↓
Clicks "Send Reset Link"
    ↓
POST /api/v1/auth/password-reset/request
    ↓
Success message shown
    ↓
User checks email
    ↓
Clicks reset link
    ↓
Redirected to /reset-password/:token
    ↓
Token validated
    ↓
User enters new password
    ↓
Clicks "Reset Password"
    ↓
POST /api/v1/auth/password-reset/confirm
    ↓
Success: Password updated
    ↓
Redirect to login
```

---

## 7. Accessibility Checklist

- [ ] All form inputs have associated `<label>` elements
- [ ] Error messages use `aria-live="polite"` for screen reader announcements
- [ ] Focus visible on all interactive elements
- [ ] Keyboard navigation works (Tab, Shift+Tab, Enter, Escape)
- [ ] Color contrast ratio ≥ 4.5:1 for text
- [ ] Form errors clearly associated with inputs (`aria-describedby`)
- [ ] Loading states announced to screen readers
- [ ] "Show password" button has proper `aria-label`
- [ ] Links have descriptive text (no "click here")
- [ ] Page has descriptive `<title>` tag

---

## 8. Testing Checklist

### Unit Tests
- [ ] Email validation works correctly
- [ ] Password strength calculation accurate
- [ ] Form submission prevents default
- [ ] Error messages display correctly
- [ ] Loading states work
- [ ] Success redirects work

### Integration Tests
- [ ] Registration creates user in database
- [ ] Login returns valid JWT
- [ ] Password reset sends email
- [ ] Email verification updates user status

### E2E Tests
- [ ] User can register → verify → login
- [ ] User can reset password successfully
- [ ] Invalid credentials show error
- [ ] Network errors handled gracefully

### Accessibility Tests
- [ ] axe DevTools reports no violations
- [ ] Keyboard navigation works
- [ ] Screen reader announces errors

---

**Maintained by**: Product & Design Team  
**Next Review**: February 14, 2026

