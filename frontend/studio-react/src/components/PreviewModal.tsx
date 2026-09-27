import React from 'react';

interface Props {
  isOpen: boolean;
  title: string;
  subtitle: string;
  onClose: () => void;
  children: React.ReactNode;
}

export const PreviewModal: React.FC<Props> = ({
  isOpen,
  title,
  subtitle,
  onClose,
  children
}) => {
  if (!isOpen) return null;

  return (
    <div
      className={`preview-modal ${isOpen ? 'visible' : ''}`}
      style={{ display: 'flex' }}
      onClick={e => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="preview-dialog">
        <div className="preview-top">
          <div className="preview-titles">
            <div className="preview-title">{title}</div>
            <div className="preview-subtitle">{subtitle}</div>
          </div>
          <button
            type="button"
            className="preview-close"
            onClick={onClose}
            aria-label="Close"
          >
            <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
        <div className="preview-body">
          {children}
        </div>
      </div>
    </div>
  );
};
