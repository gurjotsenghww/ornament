from pathlib import Path
from typing import Dict
from ornament.files.file_manager import FileManager

class PortfolioGenerator:
    """
    Scaffolds production-grade Next.js + React + TypeScript + Tailwind portfolio websites (Section 21, 23, 47).
    """

    @classmethod
    def generate(cls, workspace_path: Path, intentional_bug: bool = False) -> Dict[str, str]:
        fm = FileManager(workspace_path)

        # 1. package.json
        package_json = """{
  "name": "ornament-developer-portfolio",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.2.3",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.378.0"
  },
  "devDependencies": {
    "@types/node": "^20.12.7",
    "@types/react": "^18.3.1",
    "@types/react-dom": "^18.3.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.5"
  }
}
"""
        fm.create_file("package.json", package_json, overwrite=True)

        # 2. tsconfig.json
        tsconfig_json = """{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""
        fm.create_file("tsconfig.json", tsconfig_json, overwrite=True)

        # 3. tailwind.config.js
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#09090b",
        surface: "#18181b",
        border: "#27272a",
        accent: "#6366f1"
      }
    },
  },
  plugins: [],
}
"""
        fm.create_file("tailwind.config.js", tailwind_config, overwrite=True)

        # 4. app/globals.css
        globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: dark;
}

body {
  background-color: #09090b;
  color: #f4f4f5;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  margin: 0;
  padding: 0;
}
"""
        fm.create_file("app/globals.css", globals_css, overwrite=True)

        # 5. app/layout.tsx
        layout_tsx = """import "./globals.css";
import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata = {
  title: "Alex Vance | Senior AI & Systems Engineer",
  description: "Portfolio of Alex Vance: Autonomous systems, high-performance web applications, and local-first AI engineering.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen flex flex-col bg-background text-zinc-100 antialiased selection:bg-indigo-500 selection:text-white">
        <Navbar />
        <main className="flex-1 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
"""
        fm.create_file("app/layout.tsx", layout_tsx, overwrite=True)

        # 6. components/Navbar.tsx
        # If intentional_bug is True, introduces the route mismatch bug specified in PRD Section 14, 59:
        # points to "/contact-us" while the valid route is "/contact".
        contact_href = "/contact-us" if intentional_bug else "/contact"
        navbar_tsx = f"""import React from "react";

export default function Navbar() {{
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/80 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <a href="/" className="font-bold text-lg tracking-tight hover:text-indigo-400 transition-colors">
          Alex Vance<span className="text-indigo-500">.</span>
        </a>
        <nav aria-label="Main Navigation" className="flex items-center space-x-6 text-sm font-medium">
          <a href="/#about" className="text-zinc-400 hover:text-zinc-100 transition-colors">About</a>
          <a href="/#experience" className="text-zinc-400 hover:text-zinc-100 transition-colors">Experience</a>
          <a href="/#projects" className="text-zinc-400 hover:text-zinc-100 transition-colors">Projects</a>
          <a href="/#skills" className="text-zinc-400 hover:text-zinc-100 transition-colors">Skills</a>
          <a
            id="nav-contact-button"
            href="{contact_href}"
            className="px-4 py-2 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium transition-all shadow-sm hover:shadow-indigo-500/20"
          >
            Contact
          </a>
        </nav>
      </div>
    </header>
  );
}}
"""
        fm.create_file("components/Navbar.tsx", navbar_tsx, overwrite=True)

        # 7. components/Hero.tsx
        hero_tsx = """import React from "react";

export default function Hero() {
  return (
    <section className="py-20 sm:py-28 flex flex-col items-start justify-center">
      <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-6">
        <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
        <span>Available for Strategic Engineering</span>
      </div>
      <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white max-w-4xl leading-tight">
        Architecting autonomous agentic systems and high-throughput web infrastructure.
      </h1>
      <p className="mt-6 text-lg sm:text-xl text-zinc-400 max-w-2xl leading-relaxed">
        Specializing in local-first AI engineering, real-time compiler tooling, and high-performance React architectures.
      </p>
      <div className="mt-8 flex flex-wrap gap-4">
        <a
          href="/contact"
          className="px-6 py-3 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition-all shadow-lg shadow-indigo-600/20"
        >
          Get in Touch
        </a>
        <a
          href="#projects"
          className="px-6 py-3 rounded-lg border border-border bg-surface hover:bg-zinc-800 text-zinc-200 font-semibold transition-all"
        >
          View Case Studies
        </a>
      </div>
    </section>
  );
}
"""
        fm.create_file("components/Hero.tsx", hero_tsx, overwrite=True)

        # 8. components/About.tsx
        about_tsx = """import React from "react";

export default function About() {
  return (
    <section id="about" className="py-16 border-t border-border">
      <h2 className="text-2xl font-bold tracking-tight text-white mb-6">About Me</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-zinc-400 leading-relaxed">
        <p>
          I am a systems engineer and full-stack architect with a focus on autonomous agentic execution. My work centers on creating deterministic software tools that enable AI models to plan, execute, and verify complex engineering workflows.
        </p>
        <p>
          Passionate about zero-compromise ergonomics, strict type safety, and minimal-change surgical maintenance for mission-critical web applications.
        </p>
      </div>
    </section>
  );
}
"""
        fm.create_file("components/About.tsx", about_tsx, overwrite=True)

        # 9. components/Projects.tsx
        projects_tsx = """import React from "react";

export default function Projects() {
  const projects = [
    {
      title: "Ornàment Agent Engine",
      description: "Local-first autonomous AI software engineer capable of automated testing, minimal-change debugging, and Playwright verification.",
      tags: ["TypeScript", "Next.js", "Python", "Playwright", "Tailwind"]
    },
    {
      title: "HyperVector Store",
      description: "Ultra-low-latency in-memory vector indexing engine optimized for sub-millisecond local RAG queries.",
      tags: ["Rust", "WASM", "Information Retrieval"]
    },
    {
      title: "Aura UI Design System",
      description: "Accessible WCAG AAA component system designed for dense financial and developer dashboards.",
      tags: ["React", "Tailwind", "Radix UI", "Accessibility"]
    }
  ];

  return (
    <section id="projects" className="py-16 border-t border-border">
      <h2 className="text-2xl font-bold tracking-tight text-white mb-8">Selected Projects</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {projects.map((p, idx) => (
          <div key={idx} className="p-6 rounded-xl border border-border bg-surface hover:border-zinc-700 transition-all flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-bold text-white mb-2">{p.title}</h3>
              <p className="text-sm text-zinc-400 mb-4">{p.description}</p>
            </div>
            <div className="flex flex-wrap gap-2 mt-4">
              {p.tags.map((tag, tIdx) => (
                <span key={tIdx} className="text-xs px-2.5 py-1 rounded-md bg-zinc-800 text-zinc-300 font-mono">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
"""
        fm.create_file("components/Projects.tsx", projects_tsx, overwrite=True)

        # 10. components/Skills.tsx
        skills_tsx = """import React from "react";

export default function Skills() {
  const skillCategories = [
    { category: "Frontend & UI", items: ["React", "Next.js App Router", "TypeScript", "Tailwind CSS", "GSAP"] },
    { category: "Systems & Backend", items: ["Python", "Node.js", "FastAPI", "SQLite / PostgreSQL", "Docker"] },
    { category: "AI & Testing", items: ["Qwen Ecosystem", "Playwright", "Local RAG", "Prompt Engineering", "CI/CD"] }
  ];

  return (
    <section id="skills" className="py-16 border-t border-border">
      <h2 className="text-2xl font-bold tracking-tight text-white mb-8">Technical Expertise</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {skillCategories.map((cat, idx) => (
          <div key={idx} className="p-6 rounded-xl border border-border bg-surface">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-indigo-400 mb-4">{cat.category}</h3>
            <ul className="space-y-2">
              {cat.items.map((item, iIdx) => (
                <li key={iIdx} className="text-sm text-zinc-300 flex items-center space-x-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-zinc-600"></span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}
"""
        fm.create_file("components/Skills.tsx", skills_tsx, overwrite=True)

        # 11. components/Experience.tsx
        experience_tsx = """import React from "react";

export default function Experience() {
  const experiences = [
    {
      role: "Lead Autonomous Systems Architect",
      company: "Ornàment Labs",
      period: "2024 - Present",
      description: "Designed multi-agent execution loop with isolated file ownership, sub-agent telemetry, and Playwright verification."
    },
    {
      role: "Senior Full Stack Engineer",
      company: "Vertex Web Infrastructure",
      period: "2021 - 2024",
      description: "Spearheaded Next.js migration reducing TTFB by 42% across high-traffic engineering documentation sites."
    }
  ];

  return (
    <section id="experience" className="py-16 border-t border-border">
      <h2 className="text-2xl font-bold tracking-tight text-white mb-8">Work Experience</h2>
      <div className="space-y-6">
        {experiences.map((exp, idx) => (
          <div key={idx} className="p-6 rounded-xl border border-border bg-surface">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-2">
              <h3 className="text-lg font-bold text-white">{exp.role} · <span className="text-indigo-400">{exp.company}</span></h3>
              <span className="text-xs font-mono text-zinc-500 mt-1 sm:mt-0">{exp.period}</span>
            </div>
            <p className="text-sm text-zinc-400">{exp.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
"""
        fm.create_file("components/Experience.tsx", experience_tsx, overwrite=True)

        # 12. components/Footer.tsx
        footer_tsx = """import React from "react";

export default function Footer() {
  return (
    <footer className="border-t border-border bg-background py-8 text-center text-xs text-zinc-500">
      <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between">
        <p>© 2026 Alex Vance. Engineered with Ornàment AI Website Engineer.</p>
        <div className="flex space-x-6 mt-4 sm:mt-0">
          <a href="#" className="hover:text-zinc-300">GitHub</a>
          <a href="#" className="hover:text-zinc-300">Twitter</a>
          <a href="#" className="hover:text-zinc-300">LinkedIn</a>
        </div>
      </div>
    </footer>
  );
}
"""
        fm.create_file("components/Footer.tsx", footer_tsx, overwrite=True)

        # 13. app/page.tsx (Home page assembling all sections)
        page_tsx = """import React from "react";
import Hero from "@/components/Hero";
import About from "@/components/About";
import Experience from "@/components/Experience";
import Projects from "@/components/Projects";
import Skills from "@/components/Skills";

export default function HomePage() {
  return (
    <div className="space-y-12">
      <Hero />
      <About />
      <Experience />
      <Projects />
      <Skills />
    </div>
  );
}
"""
        fm.create_file("app/page.tsx", page_tsx, overwrite=True)

        # 14. app/contact/page.tsx (Dedicated contact page)
        contact_page_tsx = """import React from "react";

export default function ContactPage() {
  return (
    <div className="py-12 max-w-xl mx-auto">
      <h1 className="text-3xl font-bold tracking-tight text-white mb-2">Get in Touch</h1>
      <p className="text-zinc-400 mb-8">Send an inquiry regarding engineering leadership or architecture design.</p>
      
      <form className="space-y-6 p-8 rounded-2xl border border-border bg-surface shadow-xl">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-zinc-300 mb-2">Your Name</label>
          <input
            id="name"
            type="text"
            required
            className="w-full px-4 py-2.5 rounded-lg border border-border bg-zinc-900 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Ada Lovelace"
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-zinc-300 mb-2">Email Address</label>
          <input
            id="email"
            type="email"
            required
            className="w-full px-4 py-2.5 rounded-lg border border-border bg-zinc-900 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="ada@example.com"
          />
        </div>
        <div>
          <label htmlFor="message" className="block text-sm font-medium text-zinc-300 mb-2">Message</label>
          <textarea
            id="message"
            rows={4}
            required
            className="w-full px-4 py-2.5 rounded-lg border border-border bg-zinc-900 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Describe your project requirements..."
          ></textarea>
        </div>
        <button
          type="submit"
          className="w-full py-3 px-6 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition-all shadow-md hover:shadow-indigo-500/25"
        >
          Send Message
        </button>
      </form>
    </div>
  );
}
"""
        fm.create_file("app/contact/page.tsx", contact_page_tsx, overwrite=True)

        return {
            "status": "generated",
            "files_created": fm.list_files(exclude_build=True),
            "intentional_bug": str(intentional_bug)
        }
