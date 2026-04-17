export interface Line {
  slug: 'kant' | 'dostoevsky-and-literature' | 'existence-and-self' | 'moral-life'
  title: string
  tagline: string
  intro: string
  readingOrder: string[]
}

export const LINES: Line[] = [
  {
    slug: 'kant',
    title: 'Kant',
    tagline: 'Moral law, rational freedom, and why duty matters.',
    intro: 'PLACEHOLDER — fill in Phase 6.',
    readingOrder: [
      'why-we-read-kant',
      'groundwork-of-the-metaphysics-of-morals-i',
      'groundwork-of-the-metaphysics-of-morals-ii',
      'what-is-morality',
      'the-dignity-of-man',
    ],
  },
  {
    slug: 'dostoevsky-and-literature',
    title: 'Dostoevsky & Literature',
    tagline: 'Entering moral philosophy through the novel.',
    intro: 'PLACEHOLDER — fill in Phase 6.',
    readingOrder: [
      'rereading-the-brothers-karamazov',
      'reading-notes-on-the-idiot-christ-like-love',
      'humiliated-and-insulted',
      'vagabond-and-the-sublime',
      'starting-from-one-hundred-years-of-solitude',
    ],
  },
  {
    slug: 'existence-and-self',
    title: 'Existence & Self',
    tagline: 'On authenticity, subjectivity, and the life worth living.',
    intro: 'PLACEHOLDER — fill in Phase 6.',
    readingOrder: [
      'essence-of-existential-psychotherapy',
      'subjectivity-how-to-become-the-protagonist-of-your-own-life',
      'reason-and-emotion',
      'wandering-and-belonging',
      'elements-of-happiness-for-intjs',
    ],
  },
  {
    slug: 'moral-life',
    title: 'Moral Life & Public Sphere',
    tagline: 'Integrity, honesty, and courage under pressure.',
    intro: 'PLACEHOLDER — fill in Phase 6.',
    readingOrder: [
      'on-being-a-person-of-integrity',
      'do-not-lie',
      'why-discriminating-belittles-you',
      'on-human-nature-what-the-white-paper-protests-taught-me',
      'luo-xiang-a-light-flickering-against-the-wind',
    ],
  },
]

export function getLineBySlug(slug: string): Line | undefined {
  return LINES.find(l => l.slug === slug)
}
