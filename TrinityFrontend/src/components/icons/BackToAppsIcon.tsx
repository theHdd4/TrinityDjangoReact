import React from 'react';

interface BackToAppsIconProps {
  className?: string;
}

const BackToAppsIcon: React.FC<BackToAppsIconProps> = ({ className = 'w-4 h-4' }) => (
  <svg
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={2}
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <polyline points="10 8 6 12 10 16" />
    <line x1="6" y1="12" x2="22" y2="12" />
    <rect x="16" y="4" width="4" height="4" rx="1" />
    <rect x="20" y="4" width="4" height="4" rx="1" />
    <rect x="16" y="8" width="4" height="4" rx="1" />
    <rect x="20" y="8" width="4" height="4" rx="1" />
  </svg>
);

export default BackToAppsIcon;
