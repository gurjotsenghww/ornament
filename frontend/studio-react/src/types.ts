export interface CodeFile {
  id: string;
  name: string;
  lang: 'html' | 'css' | 'js' | string;
  content: string;
}

export interface Attachment {
  type: 'image' | 'doc';
  name: string;
  content?: string;
  size?: string;
  ext?: string;
  url?: string;
}

export interface ActivityFlow {
  headerLabel: string;
  doneLabel: string;
  items: string[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  text?: string;
  attachments?: Attachment[];
  activityFlow?: ActivityFlow;
  files?: CodeFile[];
  projectName?: string;
  explanation?: string;
  elapsed?: string;
  isStreaming?: boolean;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: number;
}

export interface UserProfile {
  name: string;
  photo: string;
}
