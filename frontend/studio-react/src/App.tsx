import React, { useState, useEffect, useRef } from 'react';
import type {
  Attachment,
  ActivityFlow,
  ChatMessage,
  ChatSession,
  UserProfile
} from './types';
import { CodeExplorer } from './components/CodeExplorer';
import { ActivityPanel } from './components/ActivityPanel';
import { ProfileModal } from './components/ProfileModal';
import { PreviewModal } from './components/PreviewModal';
import { getGreeting, nameToColor, isCodingTask, formatFileSize } from './utils/helpers';
import './App.css';

const QWEN_ENGINEERING_FLOW: ActivityFlow = {
  headerLabel: 'Qwen 2.5 Coder synthesizing project...',
  doneLabel: 'Website ready (Synthesized by Qwen)',
  items: [
    'Querying local Qwen2.5-Coder-3B neural model',
    'Synthesizing bespoke brand & layout architecture',
    'Applying 60-30-10 color harmonization system',
    'Writing production code bundle (HTML, CSS, JS)...',
    'Validating responsive breakpoints & accessibility'
  ]
};

const INSTANT_ENGINEERING_FLOW: ActivityFlow = {
  headerLabel: 'Instant Synthesizer generating project...',
  doneLabel: 'Website ready',
  items: [
    'Analyzing prompt tokens & visual intent',
    'Deriving optimal 60-30-10 design system',
    'Scaffolding responsive layouts & interactive widgets',
    'Writing production code bundle (HTML, CSS, JS)...',
    'Finalizing Git checkpoint & live preview'
  ]
};

export const App: React.FC = () => {
  // --- Sidebar & Profile State ---
  const [collapsed, setCollapsed] = useState<boolean>(() => {
    return localStorage.getItem('sidebarCollapsed') === 'true';
  });
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [profileModalOpen, setProfileModalOpen] = useState(false);
  const [userProfile, setUserProfile] = useState<UserProfile>(() => {
    try {
      const stored = localStorage.getItem('ornament_profile');
      if (stored) return JSON.parse(stored);
    } catch {}
    return { name: 'User', photo: '' };
  });

  // --- Modal State ---
  const [modalState, setModalState] = useState<{
    isOpen: boolean;
    title: string;
    subtitle: string;
    content: React.ReactNode;
  }>({
    isOpen: false,
    title: '',
    subtitle: '',
    content: null
  });

  // --- Model Selector ---
  const [currentModel, setCurrentModel] = useState<'qwen' | 'instant'>('qwen');
  const [modelDropdownOpen, setModelDropdownOpen] = useState(false);

  // --- Chat Sessions & Messages ---
  const [chatSessions, setChatSessions] = useState<ChatSession[]>(() => {
    try {
      const stored = localStorage.getItem('ornament_chat_sessions');
      if (stored) return JSON.parse(stored);
    } catch {}
    return [];
  });
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // --- Composer State ---
  const [promptText, setPromptText] = useState('');
  const [attachments, setAttachments] = useState<Attachment[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  // --- Activity Step Tracking ---
  const [activeStepIndex, setActiveStepIndex] = useState(0);
  const [isActivityComplete, setIsActivityComplete] = useState(false);
  const [activityElapsed, setActivityElapsed] = useState('');

  // --- Refs ---
  const chatMessagesRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const docInputRef = useRef<HTMLInputElement>(null);

  // Sync sidebarCollapsed & body classes
  useEffect(() => {
    localStorage.setItem('sidebarCollapsed', String(collapsed));
    document.body.classList.toggle('collapsed', collapsed);
  }, [collapsed]);

  useEffect(() => {
    document.body.classList.toggle('drawer-open', drawerOpen);
  }, [drawerOpen]);

  useEffect(() => {
    document.body.classList.toggle('chat-mode', messages.length > 0);
  }, [messages.length]);

  // Sync profile
  useEffect(() => {
    localStorage.setItem('ornament_profile', JSON.stringify(userProfile));
  }, [userProfile]);

  // Auto-scroll chat
  useEffect(() => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
    }
  }, [messages, activeStepIndex, isGenerating]);

  // Derive title from messages
  const deriveTitle = (msgs: ChatMessage[]): string => {
    const firstUser = msgs.find(m => m.role === 'user');
    if (firstUser && firstUser.text) {
      const t = firstUser.text.trim();
      return t.length > 40 ? t.slice(0, 40) + '…' : t;
    }
    return 'New chat';
  };

  // Save current chat session
  const saveSession = (msgs: ChatMessage[], id: string | null) => {
    if (msgs.length === 0) return;
    const sessionId = id || 'chat_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7);
    if (!id) setCurrentChatId(sessionId);

    const title = deriveTitle(msgs);
    setChatSessions(prev => {
      const idx = prev.findIndex(c => c.id === sessionId);
      let updated: ChatSession[];
      if (idx >= 0) {
        updated = [...prev];
        updated[idx] = { ...updated[idx], title, messages: msgs };
      } else {
        updated = [{ id: sessionId, title, messages: msgs, createdAt: Date.now() }, ...prev];
      }
      try {
        localStorage.setItem('ornament_chat_sessions', JSON.stringify(updated));
      } catch {}
      return updated;
    });
  };

  // Start new chat
  const handleStartNewChat = () => {
    if (messages.length > 0) {
      saveSession(messages, currentChatId);
    }
    setCurrentChatId(null);
    setMessages([]);
    setPromptText('');
    setAttachments([]);
    setDrawerOpen(false);
  };

  // Open existing chat
  const handleOpenChat = (id: string) => {
    if (id === currentChatId) return;
    if (messages.length > 0) {
      saveSession(messages, currentChatId);
    }
    const session = chatSessions.find(c => c.id === id);
    if (!session) return;
    setCurrentChatId(id);
    setMessages(session.messages);
    setDrawerOpen(false);
  };

  // Rename chat
  const handleRenameChat = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    const session = chatSessions.find(c => c.id === id);
    if (!session) return;
    const newTitle = window.prompt('Rename chat:', session.title);
    if (newTitle && newTitle.trim()) {
      const trimmed = newTitle.trim().slice(0, 60);
      setChatSessions(prev => {
        const updated = prev.map(c => c.id === id ? { ...c, title: trimmed } : c);
        try { localStorage.setItem('ornament_chat_sessions', JSON.stringify(updated)); } catch {}
        return updated;
      });
    }
  };

  // Delete chat
  const handleDeleteChat = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    setChatSessions(prev => {
      const updated = prev.filter(c => c.id !== id);
      try { localStorage.setItem('ornament_chat_sessions', JSON.stringify(updated)); } catch {}
      return updated;
    });
    if (currentChatId === id) {
      setCurrentChatId(null);
      setMessages([]);
    }
  };

  // File Upload Handlers
  const handleFilesSelected = (files: FileList | null, type: 'image' | 'doc') => {
    if (!files) return;
    Array.from(files).forEach(file => {
      const ext = file.name.split('.').pop()?.toLowerCase() || '';
      const size = formatFileSize(file.size);

      if (type === 'image') {
        const reader = new FileReader();
        reader.onload = ev => {
          setAttachments(prev => [
            ...prev,
            { type: 'image', name: file.name, url: ev.target?.result as string, size, ext }
          ]);
        };
        reader.readAsDataURL(file);
      } else {
        const reader = new FileReader();
        reader.onload = ev => {
          setAttachments(prev => [
            ...prev,
            { type: 'doc', name: file.name, content: ev.target?.result as string, size, ext }
          ]);
        };
        reader.readAsText(file);
      }
    });
  };

  // Remove attachment
  const removeAttachment = (idx: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== idx));
  };

  // Send message
  const handleSendMessage = async () => {
    const text = promptText.trim();
    if (!text && attachments.length === 0) return;
    if (isGenerating) return;

    const userMsg: ChatMessage = {
      id: 'msg_' + Date.now(),
      role: 'user',
      text: text || undefined,
      attachments: attachments.length > 0 ? [...attachments] : undefined
    };

    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setPromptText('');
    setAttachments([]);
    setIsGenerating(true);

    const isCode = isCodingTask(text) || attachments.length > 0;

    if (isCode) {
      // --- Website / Code Synthesis Route ---
      const flow = currentModel === 'qwen' ? QWEN_ENGINEERING_FLOW : INSTANT_ENGINEERING_FLOW;
      const startedAt = Date.now();
      setActiveStepIndex(0);
      setIsActivityComplete(false);
      setActivityElapsed('');

      const assistantMsgId = 'asst_' + Date.now();
      const placeholderMsg: ChatMessage = {
        id: assistantMsgId,
        role: 'assistant',
        activityFlow: flow,
        isStreaming: true
      };
      setMessages([...newMessages, placeholderMsg]);

      // Pacing interval: 5.8s for Qwen, 450ms for instant
      const intervalMs = currentModel === 'qwen' ? 5800 : 450;
      let curStep = 0;
      const stepTimer = setInterval(() => {
        if (curStep < flow.items.length - 2) {
          curStep++;
          setActiveStepIndex(curStep);
        }
      }, intervalMs);

      try {
        const res = await fetch('/api/generate-site', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prompt: text,
            attachments: userMsg.attachments?.map(a => ({
              type: a.type,
              name: a.name,
              content: a.content || '',
              size: a.size || '',
              ext: a.ext || ''
            })),
            model: currentModel
          })
        });

        clearInterval(stepTimer);
        const data = await res.json();
        const elapsed = ((Date.now() - startedAt) / 1000).toFixed(1);

        setActiveStepIndex(flow.items.length - 1);
        setIsActivityComplete(true);
        setActivityElapsed(elapsed);

        setTimeout(() => {
          const finalAssistantMsg: ChatMessage = {
            id: assistantMsgId,
            role: 'assistant',
            activityFlow: flow,
            files: data.files,
            projectName: data.project_name,
            explanation: data.explanation,
            elapsed
          };
          const updatedAll = [...newMessages, finalAssistantMsg];
          setMessages(updatedAll);
          setIsGenerating(false);
          saveSession(updatedAll, currentChatId);
        }, 500);

      } catch {
        clearInterval(stepTimer);
        const elapsed = ((Date.now() - startedAt) / 1000).toFixed(1);
        setIsActivityComplete(true);
        setActivityElapsed(elapsed);

        const errorMsg: ChatMessage = {
          id: assistantMsgId,
          role: 'assistant',
          activityFlow: flow,
          explanation: 'Backend synthesis unavailable. Please ensure the local server is running.',
          elapsed
        };
        const updatedAll = [...newMessages, errorMsg];
        setMessages(updatedAll);
        setIsGenerating(false);
        saveSession(updatedAll, currentChatId);
      }

    } else {
      // --- Conversational Chat Route ---
      const assistantMsgId = 'asst_' + Date.now();
      const streamingMsg: ChatMessage = {
        id: assistantMsgId,
        role: 'assistant',
        isStreaming: true
      };
      setMessages([...newMessages, streamingMsg]);

      try {
        const historyPayload = messages
          .filter(m => m.text)
          .slice(-10)
          .map(m => ({ role: m.role, content: m.text || '' }));

        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: text,
            history: historyPayload
          })
        });
        const data = await res.json();
        const replyText = data.reply || 'Sorry, I could not generate a response.';

        const finalMsg: ChatMessage = {
          id: assistantMsgId,
          role: 'assistant',
          text: replyText
        };
        const updatedAll = [...newMessages, finalMsg];
        setMessages(updatedAll);
        setIsGenerating(false);
        saveSession(updatedAll, currentChatId);

      } catch {
        const errorMsg: ChatMessage = {
          id: assistantMsgId,
          role: 'assistant',
          text: 'Unable to reach the model right now. Make sure the server is running on port 5050.'
        };
        const updatedAll = [...newMessages, errorMsg];
        setMessages(updatedAll);
        setIsGenerating(false);
        saveSession(updatedAll, currentChatId);
      }
    }
  };

  // Sidebar feature modals
  const handleOpenProjects = async () => {
    try {
      const res = await fetch('/api/projects');
      const list = await res.json();
      setModalState({
        isOpen: true,
        title: 'Workspace Projects',
        subtitle: `${list.length} projects stored in workspace`,
        content: (
          <div style={{ display: 'grid', gap: 12, maxHeight: 420, overflowY: 'auto' }}>
            {list.length === 0 ? (
              <p style={{ color: '#888' }}>No projects generated in workspace yet.</p>
            ) : (
              list.map((p: { name: string; path: string }) => (
                <div
                  key={p.name}
                  style={{
                    background: '#18181b',
                    border: '1px solid #27272a',
                    borderRadius: 12,
                    padding: '14px 16px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: 12
                  }}
                >
                  <div>
                    <div style={{ fontWeight: 600, color: '#fff', fontSize: 14 }}>{p.name}</div>
                    <div style={{ fontSize: 11, color: '#71717a', marginTop: 2, fontFamily: 'monospace' }}>
                      {p.path}
                    </div>
                  </div>
                  <button
                    className="ce-action"
                    onClick={() => window.open('/preview/' + encodeURIComponent(p.name), '_blank')}
                    style={{
                      padding: '6px 14px',
                      borderRadius: 8,
                      background: '#6366f1',
                      color: '#fff',
                      border: 'none',
                      cursor: 'pointer',
                      fontWeight: 600,
                      fontSize: 12
                    }}
                  >
                    Preview
                  </button>
                </div>
              ))
            )}
          </div>
        )
      });
    } catch {
      setModalState({
        isOpen: true,
        title: 'Projects',
        subtitle: 'Error loading projects',
        content: <p style={{ color: '#888' }}>Could not load project catalog.</p>
      });
    }
  };

  const handleOpenInfoModal = (title: string, subtitle: string, items: Array<{ title: string; desc: string }>) => {
    setModalState({
      isOpen: true,
      title,
      subtitle,
      content: (
        <div style={{ display: 'grid', gap: 12 }}>
          {items.map(it => (
            <div
              key={it.title}
              style={{
                background: '#18181b',
                border: '1px solid #27272a',
                borderRadius: 12,
                padding: '14px 16px'
              }}
            >
              <div style={{ fontWeight: 600, color: '#fff', fontSize: 14 }}>{it.title}</div>
              <div style={{ fontSize: 12, color: '#888', marginTop: 4 }}>{it.desc}</div>
            </div>
          ))}
        </div>
      )
    });
  };

  const { greeting, subtitle: greetingSubtitle } = getGreeting();
  const isChatMode = messages.length > 0;

  return (
    <div className={`app-root ${collapsed ? 'collapsed' : ''} ${drawerOpen ? 'drawer-open' : ''} ${isChatMode ? 'chat-mode' : ''}`} style={{ display: 'flex', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      {/* Drawer Overlay for Mobile */}
      <div className="overlay" onClick={() => setDrawerOpen(false)} />

      {/* ================= SIDEBAR ================= */}
      <aside className="sidebar">
        <div className="logo-area">
          <div className="logo">
            <span className="logo-text">Ornàment</span>
          </div>
          <button
            className="toggle-btn"
            onClick={() => setCollapsed(!collapsed)}
            aria-label="Toggle sidebar"
            title="Toggle sidebar"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="4" />
              <line x1="9" y1="3" x2="9" y2="21" />
            </svg>
          </button>
        </div>

        <nav className="nav-menu">
          <a
            href="#"
            className={`nav-item ${!isChatMode ? 'active' : ''}`}
            onClick={e => { e.preventDefault(); handleStartNewChat(); }}
          >
            <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 5v14M5 12h14" />
            </svg>
            <span>Create</span>
          </a>
          <a
            href="#"
            className="nav-item"
            onClick={e => { e.preventDefault(); handleOpenProjects(); }}
          >
            <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
            </svg>
            <span>Projects</span>
          </a>
          <a
            href="#"
            className="nav-item"
            onClick={e => {
              e.preventDefault();
              handleOpenInfoModal('Design Systems', 'Built-in 60-30-10 color harmonization engines', [
                { title: 'Electric Indigo (Default)', desc: '#6366f1 primary accent with deep neutral canvas' },
                { title: 'Emerald Studio', desc: '#10b981 natural organic contrast system' },
                { title: 'Cyber Cyan', desc: '#06b6d4 modern high-visibility engineering palette' },
                { title: 'Warm Amber', desc: '#f59e0b rich editorial typography accents' }
              ]);
            }}
          >
            <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <path d="m4.93 4.93 4.24 4.24M14.83 9.17l4.24-4.24M14.83 14.83l4.24 4.24M9.17 14.83l-4.24 4.24" />
            </svg>
            <span>Design Systems</span>
          </a>
          <a
            href="#"
            className="nav-item"
            onClick={e => {
              e.preventDefault();
              handleOpenInfoModal('Asset Library', 'Integrated generative media resources', [
                { title: 'Google Fonts Telemetry', desc: 'Preconnected Google Fonts (Instrument Serif, Space Grotesk, Plus Jakarta Sans)' },
                { title: 'Unsplash Curated CDN', desc: 'Dynamic photography placeholders with automatic query filters' },
                { title: 'Lucide & Feather SVG Icons', desc: 'Ultra-light inline vector iconography' }
              ]);
            }}
          >
            <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
              <polygon points="12 2 2 7 12 12 22 7 12 2" />
              <polyline points="2 17 12 22 22 17" />
              <polyline points="2 12 12 17 22 12" />
            </svg>
            <span>Assets</span>
          </a>
          <a
            href="#"
            className="nav-item"
            onClick={e => {
              e.preventDefault();
              handleOpenInfoModal('Deployment Targets', 'Ready-to-ship production targets', [
                { title: 'Single-Zip Export', desc: 'Static HTML5, CSS, and JS ready to drag-and-drop into Vercel or Netlify' },
                { title: 'Self-Hosted Preview Server', desc: 'Direct live preview served at /preview/{project-name}' },
                { title: 'Local Git Checkpoint', desc: 'Every build commits to an autonomous Git tracking branch' }
              ]);
            }}
          >
            <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
              <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" />
            </svg>
            <span>Deploy</span>
          </a>
        </nav>

        {/* Chat History List */}
        <div className="nav-history">
          <div className="divider" />
          <div className="nav-history-label">Recent Chats</div>
          <div className="nav-history-list">
            {chatSessions.length === 0 ? (
              <div className="nav-history-empty">No chats yet</div>
            ) : (
              chatSessions.map(c => (
                <div
                  key={c.id}
                  className={`history-item-wrap ${c.id === currentChatId ? 'active' : ''}`}
                >
                  <button
                    type="button"
                    className="history-item-btn"
                    title={c.title}
                    onClick={() => handleOpenChat(c.id)}
                  >
                    <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    </svg>
                    <span>{c.title}</span>
                  </button>
                  <div className="history-item-actions">
                    <button
                      type="button"
                      className="history-action-btn rename-btn"
                      title="Rename"
                      onClick={e => handleRenameChat(e, c.id)}
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                      </svg>
                    </button>
                    <button
                      type="button"
                      className="history-action-btn delete-btn"
                      title="Delete"
                      onClick={e => handleDeleteChat(e, c.id)}
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="3 6 5 6 21 6" />
                        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
                        <path d="M10 11v6" /><path d="M14 11v6" /><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Sidebar Bottom Profile */}
        <div className="sidebar-bottom">
          <div className="divider" />
          <a
            href="#"
            className="nav-item"
            onClick={e => {
              e.preventDefault();
              handleOpenInfoModal('Settings', 'Studio Preferences & Hardware Configuration', [
                { title: 'Neural Model', desc: 'Qwen 2.5 Coder 3B GGUF (CPU/GPU acceleration enabled)' },
                { title: 'Local Workspace', desc: 'D:\\Ornàment\\workspace (Autonomous file management)' },
                { title: 'Design Rules', desc: 'Strict 60-30-10 color balance and WCAG AAA compliance' }
              ]);
            }}
          >
            <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
            </svg>
            <span>Settings</span>
          </a>

          <div
            className="user-profile"
            title="Edit profile"
            onClick={() => setProfileModalOpen(true)}
          >
            <div
              className="avatar"
              style={{
                backgroundImage: userProfile.photo ? `url('${userProfile.photo}')` : 'none',
                backgroundColor: userProfile.photo ? '#d1d5db' : nameToColor(userProfile.name)
              }}
            >
              {!userProfile.photo && userProfile.name.charAt(0).toUpperCase()}
            </div>
            <div className="user-info">
              <span className="user-name">{userProfile.name}</span>
              <span className="user-plan">Pro Plan</span>
            </div>
            <svg className="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </div>
        </div>
      </aside>

      {/* ================= MAIN ================= */}
      <main className="main" style={{ background: "#e8ecf1 url('/bg.jpg') center/cover no-repeat fixed" }}>
        {/* Top Header */}
        <header className="top-header">
          <button
            className="hamburger"
            onClick={() => setDrawerOpen(true)}
            aria-label="Open menu"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
          <button
            className="header-toggle"
            onClick={() => setCollapsed(!collapsed)}
            aria-label="Toggle sidebar"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="4" />
              <line x1="9" y1="3" x2="9" y2="21" />
            </svg>
          </button>
        </header>

        {/* Content Area */}
        <div className="content">
          <div className="hero">
            {!isChatMode && (
              <>
                <h1 id="greetingHeading">
                  {greeting} <span className="light">{userProfile.name}.</span>
                </h1>
                <p className="subtitle" id="greetingSubtitle">
                  {greetingSubtitle}
                </p>
              </>
            )}

            {/* Chat Stream */}
            {isChatMode && (
              <div className="chat-messages" ref={chatMessagesRef}>
                {messages.map(msg => (
                  <div
                    key={msg.id}
                    className={`chat-message ${msg.role}`}
                  >
                    {/* User attachments */}
                    {msg.attachments && msg.attachments.length > 0 && (
                      <div className="attachments visible chat-message-attachments">
                        {msg.attachments.map((att, idx) => (
                          <div key={idx} className="attachment-card">
                            {att.type === 'image' && att.url && (
                              <img src={att.url} alt={att.name} className="attachment-thumb" />
                            )}
                            <div className="attachment-meta">
                              <span className="attachment-name">{att.name}</span>
                              <span className="attachment-size">{att.size}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Text bubble */}
                    {msg.text && (
                      <div
                        className="chat-bubble"
                        style={{ whiteSpace: 'pre-wrap', lineHeight: 1.65 }}
                      >
                        {msg.text}
                      </div>
                    )}

                    {/* Streaming typing dots */}
                    {msg.isStreaming && !msg.activityFlow && (
                      <div className="chat-bubble typing-dots">
                        <span /><span /><span />
                      </div>
                    )}

                    {/* Live Activity Panel */}
                    {msg.activityFlow && (
                      <ActivityPanel
                        flow={msg.activityFlow}
                        activeIndex={activeStepIndex}
                        isComplete={isActivityComplete}
                        elapsed={msg.elapsed || activityElapsed}
                      />
                    )}

                    {/* Code Explorer Bundle */}
                    {msg.files && msg.files.length > 0 && (
                      <CodeExplorer
                        files={msg.files}
                        projectName={msg.projectName}
                      />
                    )}

                    {/* Code Explanation */}
                    {msg.explanation && (
                      <div className="chat-bubble code-explanation">
                        <p>{msg.explanation}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Prompt Composer Box */}
            <div className="prompt-box">
              {/* Attachments Bar */}
              {attachments.length > 0 && (
                <div className="attachments visible">
                  {attachments.map((att, idx) => (
                    <div key={idx} className="attachment-card">
                      {att.type === 'image' && att.url && (
                        <img src={att.url} alt={att.name} className="attachment-thumb" />
                      )}
                      <div className="attachment-meta">
                        <span className="attachment-name">{att.name}</span>
                        <span className="attachment-size">{att.size}</span>
                      </div>
                      <button
                        type="button"
                        className="attachment-remove"
                        onClick={() => removeAttachment(idx)}
                      >
                        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>
                      </button>
                    </div>
                  ))}
                </div>
              )}

              <textarea
                ref={textareaRef}
                value={promptText}
                onChange={e => setPromptText(e.target.value)}
                onKeyDown={e => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage();
                  }
                }}
                className="prompt-input"
                placeholder="Ask Ornàment to build a website, code a form, or answer any question..."
                rows={1}
              />

              <div className="toolbar">
                <div className="toolbar-left">
                  <button
                    className="action-btn"
                    type="button"
                    onClick={() => imageInputRef.current?.click()}
                    title="Attach image"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                      <circle cx="8.5" cy="8.5" r="1.5" />
                      <polyline points="21 15 16 10 5 21" />
                    </svg>
                  </button>
                  <button
                    className="action-btn"
                    type="button"
                    onClick={() => docInputRef.current?.click()}
                    title="Attach document or code snippet"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                      <polyline points="14 2 14 8 20 8" />
                    </svg>
                  </button>
                </div>

                <div className="toolbar-right" style={{ position: 'relative' }}>
                  {/* Model Selector Button */}
                  <button
                    className="dropdown-btn"
                    type="button"
                    onClick={e => {
                      e.stopPropagation();
                      setModelDropdownOpen(!modelDropdownOpen);
                    }}
                    title="Select AI Synthesis Model"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="12" cy="12" r="10" />
                      <line x1="2" y1="12" x2="22" y2="12" />
                      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
                    </svg>
                    <span>{currentModel === 'qwen' ? 'Qwen 2.5 Coder' : 'Instant Synthesizer'}</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="6 9 12 15 18 9" />
                    </svg>
                  </button>

                  {/* Model Selector Popover */}
                  {modelDropdownOpen && (
                    <div
                      className="model-menu-popover"
                      style={{
                        display: 'block',
                        position: 'absolute',
                        bottom: 'calc(100% + 10px)',
                        right: 48,
                        background: 'rgba(24, 24, 28, 0.96)',
                        backdropFilter: 'blur(20px)',
                        WebkitBackdropFilter: 'blur(20px)',
                        border: '1px solid rgba(255, 255, 255, 0.12)',
                        borderRadius: 14,
                        padding: 6,
                        boxShadow: '0 16px 36px rgba(0,0,0,0.5)',
                        zIndex: 1000,
                        minWidth: 230
                      }}
                      onClick={e => e.stopPropagation()}
                    >
                      <div
                        className={`model-opt ${currentModel === 'qwen' ? 'active' : ''}`}
                        onClick={() => { setCurrentModel('qwen'); setModelDropdownOpen(false); }}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          padding: '8px 12px',
                          borderRadius: 8,
                          cursor: 'pointer',
                          color: '#fff',
                          fontSize: 13,
                          fontWeight: 500,
                          background: currentModel === 'qwen' ? 'rgba(255,255,255,0.08)' : 'transparent'
                        }}
                      >
                        <span>Qwen 2.5 Coder (Neural 3B)</span>
                        {currentModel === 'qwen' && (
                          <span style={{ color: '#6366f1', fontWeight: 'bold', marginLeft: 8 }}>✓</span>
                        )}
                      </div>
                      <div
                        className={`model-opt ${currentModel === 'instant' ? 'active' : ''}`}
                        onClick={() => { setCurrentModel('instant'); setModelDropdownOpen(false); }}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          padding: '8px 12px',
                          borderRadius: 8,
                          cursor: 'pointer',
                          color: '#8e8e9f',
                          fontSize: 13,
                          fontWeight: 500,
                          background: currentModel === 'instant' ? 'rgba(255,255,255,0.08)' : 'transparent'
                        }}
                      >
                        <span>Instant Synthesizer</span>
                        {currentModel === 'instant' && (
                          <span style={{ color: '#6366f1', fontWeight: 'bold', marginLeft: 8 }}>✓</span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Submit Button */}
                  <button
                    className="submit-btn"
                    type="button"
                    onClick={handleSendMessage}
                    disabled={isGenerating}
                    aria-label="Submit"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <line x1="12" y1="19" x2="12" y2="5" />
                      <polyline points="5 12 12 5 19 12" />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Hidden File Inputs */}
              <input
                ref={imageInputRef}
                type="file"
                accept="image/*"
                multiple
                style={{ display: 'none' }}
                onChange={e => handleFilesSelected(e.target.files, 'image')}
              />
              <input
                ref={docInputRef}
                type="file"
                accept=".pdf,.doc,.docx,.txt,.md,.html,.css,.js,.ts,.json"
                multiple
                style={{ display: 'none' }}
                onChange={e => handleFilesSelected(e.target.files, 'doc')}
              />
            </div>
          </div>
        </div>
      </main>

      {/* Profile Edit Modal */}
      <ProfileModal
        isOpen={profileModalOpen}
        profile={userProfile}
        onClose={() => setProfileModalOpen(false)}
        onSave={newProfile => {
          setUserProfile(newProfile);
          setProfileModalOpen(false);
        }}
      />

      {/* Generic Info / Preview Modal */}
      <PreviewModal
        isOpen={modalState.isOpen}
        title={modalState.title}
        subtitle={modalState.subtitle}
        onClose={() => setModalState(prev => ({ ...prev, isOpen: false }))}
      >
        {modalState.content}
      </PreviewModal>
    </div>
  );
};

export default App;
