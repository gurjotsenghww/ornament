function escapeCode(str: string): string {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

export function highlightHtml(code: string): string {
  let out = escapeCode(code);
  out = out.replace(/(&lt;!--[\s\S]*?--&gt;)/g, '<span class="tok-comment">$1</span>');
  out = out.replace(/(&lt;!DOCTYPE[^&]*?&gt;)/gi, '<span class="tok-tag">$1</span>');
  out = out.replace(/(&lt;\/?)([a-zA-Z][\w-]*)([^&]*?)(\/?&gt;)/g, (_m, open, name, attrs, close) => {
    const attrHtml = attrs.replace(
      /([a-zA-Z_:][\w:.-]*)(\s*=\s*)("[^"]*"|'[^']*')/g,
      '<span class="tok-attr">$1</span><span class="tok-punct">$2</span><span class="tok-string">$3</span>'
    );
    return '<span class="tok-tag">' + open + name + '</span>' + attrHtml + '<span class="tok-tag">' + close + '</span>';
  });
  return out;
}

export function highlightCss(code: string): string {
  let out = escapeCode(code);
  out = out.replace(/(\/\*[\s\S]*?\*\/)/g, '<span class="tok-comment">$1</span>');
  out = out.replace(/([.#]?[a-zA-Z0-9_-]+(?:[ \t]*[,>][ \t]*[.#]?[a-zA-Z0-9_-]+)*)(\s*\{)/g, '<span class="tok-selector">$1</span>$2');
  out = out.replace(/([a-zA-Z-]+)(\s*:\s*)([^;{}]+)(;)/g, '<span class="tok-prop">$1</span>$2<span class="tok-string">$3</span>$4');
  return out;
}

export function highlightJs(code: string): string {
  let out = escapeCode(code);
  out = out.replace(/(\/\/[^\n]*)/g, '<span class="tok-comment">$1</span>');
  out = out.replace(/('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|`(?:[^`\\]|\\.)*`)/g, '<span class="tok-string">$1</span>');
  out = out.replace(/\b(const|let|var|function|return|if|else|for|while|document|window|addEventListener|new|class|export|import|from|true|false|null|querySelector|querySelectorAll)\b/g, '<span class="tok-keyword">$1</span>');
  out = out.replace(/\b(\d+)\b/g, '<span class="tok-number">$1</span>');
  return out;
}

const HIGHLIGHTERS: Record<string, (code: string) => string> = {
  html: highlightHtml,
  css: highlightCss,
  js: highlightJs
};

export function renderCodeLines(content: string, lang: string): { numbers: string; body: string } {
  const highlighter = HIGHLIGHTERS[lang] || escapeCode;
  const highlighted = highlighter(content);
  const lines = highlighted.split('\n');
  const numbers = lines.map((_, i) => `<div>${i + 1}</div>`).join('');
  const body = lines.map(l => `<div>${l === '' ? '&nbsp;' : l}</div>`).join('');
  return { numbers, body };
}
