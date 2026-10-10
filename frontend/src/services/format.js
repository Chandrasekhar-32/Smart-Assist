const LABELS = {
  TEXT: 'Normal Text',
  SIMPLIFIED_TEXT: 'Simplified Explanation',
  VISUAL: 'Visual Content',
  AUDIO: 'Audio Explanation',
  SHORT_LESSON: 'Short Lesson',
}

export function formatLabel(type) {
  return LABELS[type] || type || ''
}

export const FORMAT_TYPES = Object.keys(LABELS)
