'use client';

import { FormEvent, useEffect, useState } from 'react';

type HistoryItem = {
  id: number;
  topic: string;
  tweet: string;
  style: string;
};

const writingStyles = ['Professional', 'Casual', 'Funny', 'Informative', 'Engaging'];
const starterTopics = [
  'The future of AI in healthcare',
  'Building better habits with tiny steps',
  'What makes a great creative team',
];

export default function Home() {
  const [topic, setTopic] = useState('');
  const [style, setStyle] = useState('Professional');
  const [tweet, setTweet] = useState('');
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const savedHistory = window.localStorage.getItem('tweetai-history');
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }
  }, []);

  const generateTweet = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const cleanTopic = topic.trim();

    if (!cleanTopic) {
      setError('Add a topic before generating your tweet.');
      return;
    }

    setIsGenerating(true);
    setError('');
    setCopied(false);

    try {
      const response = await fetch('/api/generate_tweet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: `${cleanTopic}\nWriting style: ${style}`,
        }),
      });

      if (!response.ok) {
        let detail = '';
        try {
          const errorBody = (await response.json()) as { detail?: string };
          detail = errorBody.detail ? ` ${errorBody.detail}` : '';
        } catch {
          // Keep the generic message when the backend does not return JSON.
        }
        throw new Error(`The generation service returned an error.${detail}`);
      }

      const result = (await response.json()) as { tweet?: string };
      if (!result.tweet) {
        throw new Error('No tweet was returned.');
      }

      setTweet(result.tweet);
      const nextHistory = [
        { id: Date.now(), topic: cleanTopic, tweet: result.tweet, style },
        ...history,
      ].slice(0, 5);
      setHistory(nextHistory);
      window.localStorage.setItem('tweetai-history', JSON.stringify(nextHistory));
    } catch (generationError) {
      setError(generationError instanceof Error ? generationError.message : 'Something went wrong.');
    } finally {
      setIsGenerating(false);
    }
  };

  const copyTweet = async () => {
    if (!tweet) return;
    await navigator.clipboard.writeText(tweet);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <main className="app-shell">
      <div className="ambient-glow ambient-glow-one" />
      <div className="ambient-glow ambient-glow-two" />

      <header className="topbar">
        <a className="brand" href="/" aria-label="TweetAI Generator home">
          <span className="brand-mark">AI</span>
          <span>TweetAI <em>Generator</em></span>
        </a>
        <nav className="topnav" aria-label="Primary navigation">
          <a className="nav-link active" href="#generator">Generate</a>
          <a className="nav-link" href="#history">History <span className="history-count">{history.length}</span></a>
        </nav>
      </header>

      <section className="hero" id="generator">
        <div className="eyebrow"><span className="eyebrow-dot" /> AI-POWERED WRITING STUDIO</div>
        <h1>Say it with <span>intention.</span></h1>
        <p className="hero-copy">Turn a thought into a tweet that sounds like you, only sharper.</p>
      </section>

      <div className="workspace-grid">
        <section className="composer-panel">
          <div className="panel-heading">
            <div>
              <p className="section-kicker">01 / Compose</p>
              <h2>What&apos;s on your mind?</h2>
            </div>
            <span className="spark-icon">✦</span>
          </div>

          <div className="suggestion-row" aria-label="Topic suggestions">
            <span className="suggestion-label">Try a spark</span>
            {starterTopics.map((starter) => (
              <button className="suggestion" key={starter} type="button" onClick={() => setTopic(starter)}>
                {starter}
              </button>
            ))}
          </div>

          <form onSubmit={generateTweet}>
            <label className="sr-only" htmlFor="topic">Tweet topic</label>
            <div className="textarea-wrap">
              <textarea
                id="topic"
                value={topic}
                onChange={(event) => {
                  setTopic(event.target.value);
                  if (error) setError('');
                }}
                placeholder="Tell us the topic, tone, and key points you want to explore..."
                maxLength={500}
              />
              <span className="input-count">{topic.length} / 500</span>
            </div>

            <div className="style-section">
              <div className="style-header">
                <label>Writing style</label>
                <span>Choose your voice</span>
              </div>
              <div className="style-options">
                {writingStyles.map((option) => (
                  <button
                    className={`style-option ${style === option ? 'selected' : ''}`}
                    key={option}
                    type="button"
                    onClick={() => setStyle(option)}
                    aria-pressed={style === option}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>

            <button className="generate-button" type="submit" disabled={isGenerating}>
              <span className="button-icon">{isGenerating ? '◌' : '✦'}</span>
              {isGenerating ? 'Thinking...' : 'Generate tweet'}
              <span className="button-arrow">↗</span>
            </button>
            {error && <p className="error-message" role="alert">{error}</p>}
          </form>
        </section>

        <section className={`result-panel ${tweet ? 'has-result' : ''}`} aria-live="polite">
          <div className="panel-heading result-heading">
            <div>
              <p className="section-kicker">02 / Refine</p>
              <h2>Your next post</h2>
            </div>
            {tweet && <span className="ready-label"><span /> Ready to share</span>}
          </div>

          {tweet ? (
            <div className="result-content">
              <blockquote>{tweet}</blockquote>
              <div className="result-meta">
                <span>{tweet.length} characters</span>
                <span className="meta-divider" />
                <span>{style} voice</span>
                <button className="copy-button" type="button" onClick={copyTweet}>
                  {copied ? 'Copied' : 'Copy tweet'} <span>{copied ? '✓' : '↗'}</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="empty-result">
              <div className="empty-orbit"><span>✦</span></div>
              <p>Your finished thought<br /><strong>will appear here.</strong></p>
              <span className="empty-hint">A little clarity goes a long way.</span>
            </div>
          )}
        </section>
      </div>

      <section className="history-section" id="history">
        <div className="history-heading">
          <div>
            <p className="section-kicker">03 / Archive</p>
            <h2>Recent generations</h2>
          </div>
          <span className="archive-note">Saved in this browser</span>
        </div>
        {history.length ? (
          <div className="history-list">
            {history.map((item) => (
              <button className="history-item" key={item.id} type="button" onClick={() => { setTopic(item.topic); setTweet(item.tweet); setStyle(item.style); }}>
                <span className="history-item-topic">{item.topic}</span>
                <span className="history-item-tweet">{item.tweet}</span>
                <span className="history-item-arrow">↗</span>
              </button>
            ))}
          </div>
        ) : (
          <div className="history-empty">Your first generated tweet will be kept here for easy reference.</div>
        )}
      </section>

      <footer className="footer"><span>TweetAI / 2026</span><span>Made for thoughts worth sharing.</span></footer>
    </main>
  );
}
