/**
 * Mic toggle. Edge dictates live. Firefox records, then transcribes.
 */

import React from 'react';
import { Mic, MicOff } from 'lucide-react';

export default function MicButton({
  supported,
  listening,
  phase = 'idle',
  onToggle,
  title,
  className = '',
  size = 15,
}) {
  if (!supported) {
    return (
      <button
        type="button"
        disabled
        title="Voice input is not supported in this browser"
        aria-label="Voice input unavailable"
        className={`tap grid h-11 w-11 shrink-0 place-items-center rounded-sm border border-rule text-text-faint opacity-50 lg:h-9 lg:w-9 ${className}`}
      >
        <MicOff size={size} />
      </button>
    );
  }

  const working = phase === 'loading' || phase === 'transcribing';
  const active = listening || working;
  const label = phase === 'loading'
    ? 'Loading speech model'
    : phase === 'transcribing'
      ? 'Transcribing'
      : listening
        ? 'Stop voice input'
        : 'Start voice input';

  return (
    <button
      type="button"
      onClick={onToggle}
      disabled={working}
      title={title ?? (phase === 'loading'
        ? 'Loading the speech model'
        : phase === 'transcribing'
          ? 'Transcribing'
          : listening
            ? 'Stop listening'
            : 'Dictate with voice')}
      aria-label={label}
      aria-pressed={active}
      aria-busy={working}
      className={`tap grid h-11 w-11 shrink-0 place-items-center rounded-sm border transition-colors lg:h-9 lg:w-9 ${
        active
          ? 'border-critical bg-critical text-on-ink'
          : 'border-ink bg-paper text-text hover:bg-ink hover:text-on-ink'
      } ${working ? 'opacity-80' : ''} ${className}`}
    >
      <Mic size={size} className={listening ? 'live-dot' : ''} />
    </button>
  );
}
