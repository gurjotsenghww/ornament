import React, { useState, useRef, useEffect } from 'react';
import type { UserProfile } from '../types';

interface Props {
  isOpen: boolean;
  profile: UserProfile;
  onClose: () => void;
  onSave: (newProfile: UserProfile) => void;
}

export const ProfileModal: React.FC<Props> = ({
  isOpen,
  profile,
  onClose,
  onSave
}) => {
  const [name, setName] = useState(profile.name);
  const [photo, setPhoto] = useState(profile.photo);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setName(profile.name);
    setPhoto(profile.photo);
  }, [profile, isOpen]);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      setPhoto(ev.target?.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleSave = () => {
    onSave({
      name: name.trim() || 'User',
      photo
    });
  };

  return (
    <div
      id="profileModal"
      style={{
        display: 'flex',
        position: 'fixed',
        inset: 0,
        zIndex: 9000,
        background: 'rgba(0,0,0,0.45)',
        backdropFilter: 'blur(6px)',
        WebkitBackdropFilter: 'blur(6px)',
        alignItems: 'center',
        justifyContent: 'center'
      }}
      onClick={e => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        style={{
          background: '#fff',
          borderRadius: 20,
          padding: '32px 28px',
          width: '100%',
          maxWidth: 380,
          boxShadow: '0 24px 60px rgba(0,0,0,0.2)',
          position: 'relative',
          margin: 20
        }}
      >
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: 14,
            right: 14,
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            color: '#888',
            padding: 6,
            borderRadius: 8,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
          aria-label="Close"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 6, letterSpacing: '-0.3px' }}>
          Edit Profile
        </h2>
        <p style={{ fontSize: 13, color: '#888', marginBottom: 24 }}>
          Your name and photo appear everywhere in the studio.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12, marginBottom: 24 }}>
          <div
            onClick={() => fileInputRef.current?.click()}
            style={{
              width: 80,
              height: 80,
              borderRadius: '50%',
              backgroundColor: '#e8ecf1',
              backgroundImage: photo ? `url('${photo}')` : 'none',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              border: '3px solid #f0f0f0',
              boxShadow: '0 2px 12px rgba(0,0,0,0.1)',
              cursor: 'pointer',
              position: 'relative',
              overflow: 'hidden',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            {!photo && (
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#aaa" strokeWidth="1.5" strokeLinecap="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            )}
          </div>
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            style={{
              fontSize: 13,
              color: '#6366f1',
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
              fontWeight: 500,
              padding: '4px 0'
            }}
          >
            Change photo
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </div>

        <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: '#555', marginBottom: 6, letterSpacing: 0.3 }}>
          DISPLAY NAME
        </label>
        <input
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') handleSave(); }}
          placeholder="Enter your name"
          maxLength={40}
          style={{
            width: '100%',
            padding: '11px 14px',
            border: '1.5px solid #e5e5e5',
            borderRadius: 10,
            fontSize: 14,
            fontFamily: 'inherit',
            outline: 'none',
            color: '#111',
            background: '#fafafa',
            boxSizing: 'border-box'
          }}
        />

        <button
          type="button"
          onClick={handleSave}
          style={{
            marginTop: 20,
            width: '100%',
            padding: 12,
            background: '#111',
            color: '#fff',
            border: 'none',
            borderRadius: 10,
            fontSize: 14,
            fontWeight: 600,
            cursor: 'pointer',
            fontFamily: 'inherit',
            transition: 'background 0.15s'
          }}
        >
          Save changes
        </button>
      </div>
    </div>
  );
};
