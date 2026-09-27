import React, { useState, useMemo } from 'react';
import type { CodeFile } from '../types';
import { renderCodeLines } from '../utils/syntax';
import { downloadZip } from '../utils/zip';

interface Props {
  files: CodeFile[];
  projectName?: string;
}

export const CodeExplorer: React.FC<Props> = ({ files, projectName }) => {
  const [view, setView] = useState<'code' | 'preview'>('code');
  const [activeFileId, setActiveFileId] = useState<string>(files[0]?.id || 'html');
  const [copied, setCopied] = useState(false);

  const activeFile = files.find(f => f.id === activeFileId) || files[0];

  const { numbers, body } = useMemo(() => {
    if (!activeFile) return { numbers: '', body: '' };
    return renderCodeLines(activeFile.content, activeFile.lang);
  }, [activeFile]);

  const previewDoc = useMemo(() => {
    const htmlFile = files.find(f => f.lang === 'html' || f.name.endsWith('.html'));
    const cssFile = files.find(f => f.lang === 'css' || f.name.endsWith('.css'));
    const jsFile = files.find(f => f.lang === 'js' || f.name.endsWith('.js'));

    let html = htmlFile ? htmlFile.content : '<!DOCTYPE html><html><body><p>No HTML</p></body></html>';
    if (cssFile) {
      if (html.includes('</head>')) {
        html = html.replace('</head>', `<style>\n${cssFile.content}\n</style>\n</head>`);
      } else {
        html = `<style>\n${cssFile.content}\n</style>\n` + html;
      }
    }
    if (jsFile) {
      if (html.includes('</body>')) {
        html = html.replace('</body>', `<script>\n${jsFile.content}\n<\/script>\n</body>`);
      } else {
        html += `\n<script>\n${jsFile.content}\n<\/script>`;
      }
    }
    return html;
  }, [files]);

  const handleCopy = () => {
    if (!activeFile) return;
    navigator.clipboard.writeText(activeFile.content).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  };

  const handleDownload = () => {
    downloadZip(files, (projectName || 'project') + '.zip');
  };

  return (
    <div className="chat-bubble code-explorer-bubble">
      <div className="code-explorer">
        <div className="ce-topbar">
          <div className="ce-toggle">
            <button
              type="button"
              className={`ce-toggle-btn ${view === 'preview' ? 'active' : ''}`}
              onClick={() => setView('preview')}
            >
              <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
              Preview
            </button>
            <button
              type="button"
              className={`ce-toggle-btn ${view === 'code' ? 'active' : ''}`}
              onClick={() => setView('code')}
            >
              <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="16 18 22 12 16 6" />
                <polyline points="8 6 2 12 8 18" />
              </svg>
              Code
            </button>
          </div>

          <div className="ce-topbar-right">
            <span className="ce-lang">
              {activeFile?.lang.toUpperCase()}
            </span>
            <button
              type="button"
              className={`ce-action ${copied ? 'copied' : ''}`}
              onClick={handleCopy}
            >
              <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
              </svg>
              <span className="ce-label">{copied ? 'Copied' : 'Copy'}</span>
            </button>
            <button
              type="button"
              className="ce-action"
              onClick={handleDownload}
            >
              <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
              </svg>
              Download
            </button>
            <button
              type="button"
              className="ce-run"
              onClick={() => setView('preview')}
            >
              <svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3" /></svg>
              Run
            </button>
          </div>
        </div>

        <div className="ce-tabs">
          {files.map(f => (
            <button
              key={f.id}
              type="button"
              className={`ce-tab ${f.id === activeFileId ? 'active' : ''}`}
              data-file={f.lang}
              onClick={() => setActiveFileId(f.id)}
            >
              <span className="ce-tab-icon">
                {f.lang === 'html' && (
                  <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" /></svg>
                )}
                {f.lang === 'css' && '#'}
                {f.lang === 'js' && 'JS'}
              </span>
              {f.name}
            </button>
          ))}
        </div>

        <div className="ce-body">
          <div className={`ce-code-view ${view === 'preview' ? 'hidden' : ''}`}>
            <pre className="ce-code">
              <span className="ce-line-numbers" dangerouslySetInnerHTML={{ __html: numbers }} />
              <span className="ce-code-lines" dangerouslySetInnerHTML={{ __html: body }} />
            </pre>
          </div>
          <div className={`ce-preview-view ${view === 'preview' ? 'active' : ''}`}>
            <iframe
              className="ce-iframe"
              sandbox="allow-scripts allow-modals"
              srcDoc={previewDoc}
              title="Live Preview"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
