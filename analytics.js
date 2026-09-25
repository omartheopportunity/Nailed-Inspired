// Vercel Web Analytics for Static HTML Sites
// This module initializes Vercel Web Analytics tracking
// When deployed to Vercel, the platform automatically injects the actual tracking script

// The window.va function has already been initialized in the HTML <head> tag
// This ensures all pageviews are tracked automatically

// For custom event tracking, use:
// window.va('event', { name: 'custom-event-name' });

export default function initAnalytics() {
  // Automatically track page views when deployed to Vercel
  // No additional configuration needed
  if (typeof window !== 'undefined' && window.va) {
    console.log('Vercel Analytics initialized');
  }
}

// Auto-initialize on module load
if (typeof window !== 'undefined') {
  initAnalytics();
}
