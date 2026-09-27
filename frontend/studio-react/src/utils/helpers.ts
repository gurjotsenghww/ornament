export function getGreeting(): { greeting: string; subtitle: string } {
  const hour = new Date().getHours();
  if (hour < 5)  return { greeting: 'Good night,',     subtitle: "Still up? Let's build something." };
  if (hour < 12) return { greeting: 'Good morning,',   subtitle: 'What are we building today?' };
  if (hour < 17) return { greeting: 'Good afternoon,', subtitle: 'Ready to bring your next idea to life?' };
  if (hour < 22) return { greeting: 'Good evening,',   subtitle: "What's cookin' in your mind tonight?" };
  return             { greeting: 'Good night,',         subtitle: "Still up? Let's build something." };
}

export function nameToColor(name: string): string {
  const palette = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#14b8a6'];
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return palette[Math.abs(hash) % palette.length];
}

export function isCodingTask(prompt: string): boolean {
  if (!prompt) return false;
  const p = prompt.toLowerCase();
  const siteWords = [
    'build', 'create', 'make', 'generate', 'design', 'develop', 'code',
    'website', 'webpage', 'web page', 'landing page', 'landing-page',
    'portfolio', 'blog', 'app', 'application', 'site', 'homepage',
    'html', 'css', 'javascript', 'js', 'react', 'vue', 'svelte',
    'ui', 'frontend', 'backend', 'component', 'button', 'form',
    'navbar', 'footer', 'hero section', 'e-commerce', 'ecommerce',
    'dashboard', 'admin panel', 'saas', 'payment page', 'checkout'
  ];
  return siteWords.some(w => p.includes(w));
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}
