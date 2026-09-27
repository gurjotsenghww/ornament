import React, { useState } from 'react';
import type { ActivityFlow } from '../types';

interface Props {
  flow: ActivityFlow;
  activeIndex: number;
  isComplete: boolean;
  elapsed?: string;
}

export const ActivityPanel: React.FC<Props> = ({
  flow,
  activeIndex,
  isComplete,
  elapsed
}) => {
  const [collapsed, setCollapsed] = useState(isComplete);

  return (
    <div className={`activity-panel ${collapsed ? 'collapsed' : ''}`}>
      <button
        className="activity-header"
        type="button"
        aria-expanded={!collapsed}
        onClick={() => setCollapsed(!collapsed)}
      >
        <span className="activity-sparkle">
          <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 3l1.8 5.3L19 10l-5.2 1.7L12 17l-1.8-5.3L5 10l5.2-1.7L12 3z" />
            <path d="M19 16l.9 2.1L22 19l-2.1.9L19 22l-.9-2.1L16 19l2.1-.9L19 16z" />
          </svg>
        </span>
        <span className="activity-status">
          {isComplete ? flow.doneLabel : flow.headerLabel}
        </span>
        {isComplete && elapsed && (
          <span className="activity-meta">{elapsed}s</span>
        )}
        <svg className="activity-chevron" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      <div className="activity-body">
        <div className="activity-list">
          {flow.items.map((label, idx) => {
            const state = isComplete || idx < activeIndex
              ? 'done'
              : idx === activeIndex
              ? 'active'
              : 'upcoming';

            return (
              <div
                key={label}
                className="activity-item"
                data-index={idx}
                data-state={state}
              >
                <span className="activity-circle">
                  <svg className="icon-check" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </span>
                <span className="activity-label">{label}</span>
                <div className="activity-progress-wrap">
                  <div
                    className="activity-progress-bar"
                    style={{
                      width: state === 'done' ? '100%' : state === 'active' ? '85%' : '0%'
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
